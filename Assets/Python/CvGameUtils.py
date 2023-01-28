###	Imports
from CvPythonExtensions import *
import CvEventInterface
import CvUtil
import ThreatUtil
import WidgetUtil

import HR
import HR_Map
import HR_Organizations
import HR_Religion
import CivilWar



### Constants
gc = CyGlobalContext()



class CvGameUtils:
	"Miscellaneous game functions"
	def __init__(self):
		pass



	def isVictoryTest(self):
		if gc.getGame().getElapsedGameTurns() > 10:
			return True
		else:
			return False



	def isVictory(self, argsList):
		eVictory = argsList[0]
		return True



	def isPlayerResearch(self, argsList):
		ePlayer = argsList[0]
		return True



	def getExtraCost(self, argsList):
		ePlayer = argsList[0]
		return 0



	def createBarbarianCities(self):
		return False



	def createBarbarianUnits(self):
		return False



	def skipResearchPopup(self, argsList):
		ePlayer = argsList[0]
		return False



	def showTechChooserButton(self, argsList):
		ePlayer = argsList[0]
		return True



	def getFirstRecommendedTech(self, argsList):
		ePlayer = argsList[0]
		return TechTypes.NO_TECH



	def getSecondRecommendedTech(self, argsList):
		ePlayer = argsList[0]
		eFirstTech = argsList[1]
		return TechTypes.NO_TECH



	def canRazeCity(self, argsList):
		iRazingPlayer, pCity = argsList
		return True



	def canDeclareWar(self, argsList):
		iAttackingTeam, iDefendingTeam = argsList
		return True



	def skipProductionPopup(self, argsList):
		pCity = argsList[0]
		return False



	def showExamineCityButton(self, argsList):
		pCity = argsList[0]
		return True



	def getRecommendedUnit(self, argsList):
		pCity = argsList[0]
		return UnitTypes.NO_UNIT



	def getRecommendedBuilding(self, argsList):
		pCity = argsList[0]
		return BuildingTypes.NO_BUILDING



	def updateColoredPlots(self):
		return False



	def isActionRecommended(self, argsList):
		pUnit = argsList[0]
		iAction = argsList[1]
		return False



	def unitCannotMoveInto(self, argsList):
		ePlayer = argsList[0]
		iUnitId = argsList[1]
		iPlotX = argsList[2]
		iPlotY = argsList[3]
		return False



	def cannotHandleAction(self, argsList):
		pPlot = argsList[0]
		iAction = argsList[1]
		bTestVisible = argsList[2]
		return False



	def canBuild(self, argsList):
		'-1  - ignore'
		' 0  - build cannot be performed'
		' 1+ - build can be performed'
		iX, iY, iBuild, iPlayer = argsList

		# Forts
		if iBuild == gc.getInfoTypeForString('BUILD_FORT'):
			pPlot = CyMap().plot(iX, iY)
			if HR_Map.getNumAdjacentImprovement(pPlot, gc.getInfoTypeForString('IMPROVEMENT_FORT'), 1) > 0:
				return 0

		# Routes
		if iBuild == gc.getInfoTypeForString('BUILD_RAILROAD'):
			if CyMap().plot(iX, iY).getRouteType() == gc.getInfoTypeForString('ROUTE_HIGHWAY'):
				return 1

		return -1



	def cannotFoundCity(self, argsList):
		iPlayer, iPlotX, iPlotY = argsList
		return False



	def cannotSelectionListMove(self, argsList):
		pPlot = argsList[0]
		bAlt = argsList[1]
		bShift = argsList[2]
		bCtrl = argsList[3]
		return False



	def cannotSelectionListGameNetMessage(self, argsList):
		eMessage = argsList[0]
		iData2 = argsList[1]
		iData3 = argsList[2]
		iData4 = argsList[3]
		iFlags = argsList[4]
		bAlt = argsList[5]
		bShift = argsList[6]
		return False



	def cannotDoControl(self, argsList):
		eControl = argsList[0]
		return False


	def canResearch(self, argsList):
		ePlayer = argsList[0]
		eTech = argsList[1]
		bTrade = argsList[2]
		return False



	def cannotResearch(self, argsList):
		ePlayer = argsList[0]
		eTech = argsList[1]
		bTrade = argsList[2]
		return False



	def canDoCivic(self, argsList):
		ePlayer = argsList[0]
		eCivic = argsList[1]
		return False



	def cannotDoCivic(self, argsList):
		iPlayer = argsList[0]
		iCivic = argsList[1]
		pPlayer = gc.getPlayer(iPlayer)

	### Tenets
		if not pPlayer.isCivic(iCivic):
			if HR_Religion.Tenets().isTenet(iCivic):
				return True
			elif not pPlayer.isHuman() and not pPlayer.isBarbarian():
				if HR_Religion.Tenets().getReformationTimer(pPlayer) > 0:
					return True
		###

		return False



	def canTrain(self, argsList):
		pCity = argsList[0]
		eUnit = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		bIgnoreUpgrades = argsList[5]
		return False



	def cannotTrain(self, argsList):
		pCity = argsList[0]
		iUnit = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		bIgnoreUpgrades = argsList[5]

		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		UnitInfo = gc.getUnitInfo(iUnit)

		# Work Boats (stop the AI stockpiling them)
		if UnitInfo.getDefaultUnitAIType() == gc.getInfoTypeForString('UNITAI_WORKER_SEA'):
			if not pPlayer.isHuman():
				pArea = pCity.waterArea()
				nWorkboats = pArea.getNumAIUnits(iPlayer, gc.getInfoTypeForString('UNITAI_WORKER_SEA'))
				nResources = pPlayer.countUnimprovedBonuses(pArea, pCity.plot())
				if nWorkboats > nResources:
					return True

		# Missionaries
		elif UnitInfo.getPrereqReligion() > -1:
			iLimit = HR_Religion.getMaxReligiousUnit()
			iTrain = pPlayer.getUnitClassCountPlusMaking(UnitInfo.getUnitClassType())
			if pCity.getProductionUnit() == iUnit and iTrain == iLimit:
				return False
			elif iTrain >= iLimit:
				return True

		# Inquisitors
		elif iUnit == HR_Religion.Inquisition().InquisitorUnit:
			if not pPlayer.isCivic(HR_Religion.Tenets().AllowInquisitors):
				return True
			else:
				iLimit = HR_Religion.getMaxReligiousUnit()
				iTrain = pPlayer.getUnitClassCountPlusMaking(UnitInfo.getUnitClassType())
				if pCity.getProductionUnit() == iUnit and iTrain == iLimit:
					return False
				elif iTrain >= iLimit:
					return True

		# Executives
		elif UnitInfo.getPrereqCorporation() > -1:
			if pCity.isHeadquartersByType(UnitInfo.getPrereqCorporation()):
				iLimit = HR_Organizations.getMaxOrganizationUnit()
				iTrain = pPlayer.getUnitClassCountPlusMaking(UnitInfo.getUnitClassType())
				if pCity.getProductionUnit() == iUnit and iTrain == iLimit:
					return False
				elif iTrain >= iLimit:
					return True

			else:
				return True

		return False



	def canConstruct(self, argsList):
		pCity = argsList[0]
		iBuilding = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		return False



	def cannotConstruct(self, argsList):
		pCity = argsList[0]
		eBuilding = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]

	### Monasteries
		BuildingInfo = gc.getBuildingInfo(eBuilding)
		if BuildingInfo.getType().find("_MONASTERY_") > 0:
			iReligion = BuildingInfo.getPrereqReligion()
			if not HR_Religion.canConstructMonastery(pCity, iReligion):
				return True

	### Water Well
		if eBuilding == gc.getInfoTypeForString('BUILDING_WELL'):
			if pCity.isCoastal(1) or pCity.plot().isRiverSide():
				return True

	### Wonders
		iBuildingClass = BuildingInfo.getBuildingClassType()
		if not CyGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE):
			if isWorldWonderClass(iBuildingClass):
				if BuildingInfo.getFoundsCorporation() == -1:
					if pCity.getNumWorldWonders() >= HR.getWorldWonderLimit(pCity):
						return True

	### Hagia Sophia
		pPlayer = gc.getPlayer(pCity.getOwner())
		if pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_HAGIA_SOPHIA')) > 0:
			for iPlayerX in xrange(gc.getMAX_CIV_PLAYERS()):
				pPlayerX = gc.getPlayer(iPlayerX)
				if pPlayerX.isEverAlive():
					iBuilding = gc.getCivilizationInfo(pPlayerX.getCivilizationType()).getCivilizationBuildings(iBuildingClass)
					if pCity.getNumActiveBuilding(iBuilding):
						return True
		###
		return False



	def canCreate(self, argsList):
		pCity = argsList[0]
		eProject = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		return False



	def cannotCreate(self, argsList):
		pCity = argsList[0]
		eProject = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		return False



	def canMaintain(self, argsList):
		pCity = argsList[0]
		eProcess = argsList[1]
		bContinue = argsList[2]

	### Traits - Always Build Commerce
		if eProcess in HR.Trait.AlwaysBuildCommerce.keys():
			iTrait = HR.Trait.AlwaysBuildCommerce[eProcess]
			pPlayer = gc.getPlayer(pCity.getOwner())
			if pPlayer.hasTrait(iTrait):
				return True
		###
		return False



	def cannotMaintain(self, argsList):
		pCity = argsList[0]
		eProcess = argsList[1]
		bContinue = argsList[2]

	### Traits - Always Build Commerce
		pPlayer = gc.getPlayer(pCity.getOwner())
		for iProcess, iTrait in HR.Trait.AlwaysBuildCommerce.iteritems():
			if pPlayer.hasTrait(iTrait) and eProcess != iProcess:
				if gc.getProcessInfo(eProcess).getButton() == gc.getProcessInfo(iProcess).getButton():
					return True


	### Process Ranks
		# Skip if this process is the very last one in the list
		if eProcess < (gc.getNumProcessInfos() - 1):
			# Check if there is a higher rank for this commerce type (by comparing buttons)
			if gc.getProcessInfo(eProcess).getButton() == gc.getProcessInfo(eProcess + 1).getButton():
				# Disable this process if team has the tech to unlock the next rank
				iTech = gc.getProcessInfo(eProcess + 1).getTechPrereq()
				if gc.getTeam(pPlayer.getTeam()).isHasTech(iTech):
					return True
		###
		return False



	def AI_chooseTech(self, argsList):
		ePlayer = argsList[0]
		bFree = argsList[1]
		return TechTypes.NO_TECH



	def AI_chooseProduction(self, argsList):
		pCity = argsList[0]
		pPlayer = gc.getPlayer(pCity.getOwner())

	### Inquisition - AI
		if CyGame().isVictoryValid(gc.getInfoTypeForString('VICTORY_RELIGIOUS')):
			if pPlayer.isCivic(HR_Religion.Tenets().AllowInquisitors):
				if pCity.getProduction() == 0:
					if CyGame().getSorenRandNum(5, "Chance to Train Inquisitor") == 0:
						if HR_Religion.Inquisition().shouldTrainInquisitor(pCity, pCity.getOwner()):
							iInquisitor = HR_Religion.Inquisition().InquisitorUnit
							if pCity.canTrain(iInquisitor, True, False):
								pCity.pushOrder(OrderTypes.ORDER_TRAIN, iInquisitor , -1, False, True, False, True)
								return True
		###
		return False



	def AI_unitUpdate(self, argsList):
		pUnit = argsList[0]

	### Great Doctor
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_DOCTOR'):
			if CivilWar.CivilWar().doHumanitarianMissionAI(pUnit):
				return True

	### Inquisitor
		elif pUnit.getUnitType() == HR_Religion.Inquisition().InquisitorUnit:
			HR_Religion.Inquisition().doInquisitorAI(pUnit, pUnit.getOwner())
			return True
		###
		return False



	def AI_doWar(self, argsList):
		eTeam = argsList[0]
		return False



	def AI_doDiplo(self, argsList):
		ePlayer = argsList[0]
		return False



	def calculateScore(self, argsList):
		ePlayer = argsList[0]
		bFinal = argsList[1]
		bVictory = argsList[2]

		iPopulationScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getPopScore(), gc.getGame().getInitPopulation(), gc.getGame().getMaxPopulation(), gc.getDefineINT("SCORE_POPULATION_FACTOR"), True, bFinal, bVictory)
		iLandScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getLandScore(), gc.getGame().getInitLand(), gc.getGame().getMaxLand(), gc.getDefineINT("SCORE_LAND_FACTOR"), True, bFinal, bVictory)
		iTechScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getTechScore(), gc.getGame().getInitTech(), gc.getGame().getMaxTech(), gc.getDefineINT("SCORE_TECH_FACTOR"), True, bFinal, bVictory)
		iWondersScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getWondersScore(), gc.getGame().getInitWonders(), gc.getGame().getMaxWonders(), gc.getDefineINT("SCORE_WONDER_FACTOR"), False, bFinal, bVictory)
		return int(iPopulationScore + iLandScore + iWondersScore + iTechScore)



	def doHolyCity(self):
		return False



	def doHolyCityTech(self, argsList):
		eTeam = argsList[0]
		ePlayer = argsList[1]
		eTech = argsList[2]
		bFirst = argsList[3]
		return False



	def doGoody(self, argsList):
		ePlayer = argsList[0]
		pPlot = argsList[1]
		pUnit = argsList[2]
		return False



	def doGold(self, argsList):
		ePlayer = argsList[0]
		return False



	def doResearch(self, argsList):
		ePlayer = argsList[0]
		return False



	def doGrowth(self, argsList):
		pCity = argsList[0]

	### Starvation Dissent
		if pCity.getFood() + pCity.foodDifference(True) < 0:
			HR.setCityData(pCity, HR.CityData.index('STARVATION'), "1")

		return False



	def doProduction(self, argsList):
		pCity = argsList[0]
		return False



	def doCulture(self, argsList):
		pCity = argsList[0]
		pPlayer = gc.getPlayer(pCity.getOwner())

	### Culture Over Trade Routes
		if not pPlayer.isCivic(HR.Civic.NoTradeRouteCulture):
			for i in xrange(pCity.getTradeRoutes()):
				pTradeCity = pCity.getTradeCity(i)
				if not pTradeCity.isNone():
					iCulture = HR.getCultureTransfer(pCity, pTradeCity)
					if iCulture > 0:
						pCity.changeCulture(pTradeCity.getOwner(), iCulture, True)

		return False



	def doPlotCulture(self, argsList):
		pCity = argsList[0]
		bUpdate = argsList[1]
		ePlayer = argsList[2]
		iCultureRate = argsList[3]
		return False



	def doReligion(self, argsList):
		pCity = argsList[0]
		return False



	def cannotSpreadReligion(self, argsList):
		iOwner, iUnitID, iReligion, iX, iY = argsList
		return False



	def doGreatPeople(self, argsList):
		pCity = argsList[0]
		pPlayer = gc.getPlayer(pCity.getOwner())

	### Great People - Separate Pools
		if pCity.isDisorder():
			return True

		sProgress = ""
		GPProgress = HR.getCityData(pCity, HR.CityData.index('GREAT_PEOPLE_PROGRESS')).split(",")
		pCity.changeGreatPeopleProgress(pCity.getGreatPeopleRate()) # For AI valuation

		for i in xrange(len(HR.GreatPeople)):
			iUnit = HR.GreatPeople[i]
			iModifier = HR.getGreatPersonModifier(pCity, iUnit)
			iProgress = int(GPProgress[i]) + pCity.getGreatPeopleUnitRate(iUnit)
			iProgress += (pCity.getGreatPeopleUnitRate(iUnit) * iModifier) / 100

			if iProgress >= pPlayer.greatPeopleThreshold(False):
				iProgress -= pPlayer.greatPeopleThreshold(False)
				pCity.changeGreatPeopleProgress(-pPlayer.greatPeopleThreshold(False)) # For AI valuation
				pCity.createGreatPeople(iUnit, True, False)

			sProgress += str(iProgress)
			if iUnit != HR.GreatPeople[-1]:
				sProgress += ","

		HR.setCityData(pCity, HR.CityData.index('GREAT_PEOPLE_PROGRESS'), sProgress)
		return True



	def doMeltdown(self, argsList):
		pCity = argsList[0]

		# Callback disabled for Windows, handled in the DLL instead
		eNuclearPlant = gc.getInfoTypeForString('BUILDING_NUCLEAR_PLANT')
		if pCity.getNumBuilding(eNuclearPlant) > 0:
			iMeltdownChance = gc.getBuildingInfo(eNuclearPlant).getNukeExplosionRand()
			if CyGame().getSorenRandNum(iMeltdownChance, "Meltdown!!!") == 0:
				pCity.setNumRealBuilding(eNuclearPlant, 0)
				PlotList = HR_Map.getAdjacentPlots(pCity.plot(), 1, False)
				for pPlot in PlotList:
					if not pPlot.isWater() and not pPlot.isImpassable():
						iFeature = pPlot.getFeatureType()
						if iFeature == -1 or not gc.getFeatureInfo(iFeature).isNukeImmune():
							if CyGame().getSorenRandNum(100, "Nuke Fallout") < gc.getDefineINT('NUKE_FALLOUT_PROB'):
								pPlot.setImprovementType(-1)
								pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_FALLOUT'), 0)

				CyInterface().addMessage(pCity.getOwner(), True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText('TXT_KEY_MISC_MELTDOWN_CITY', (pCity.getName(), )), 'AS2D_MELTDOWN', InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, CyArtFileMgr().getInterfaceArtInfo('INTERFACE_UNHEALTHY_PERSON').getPath(), ColorTypes(gc.getInfoTypeForString('COLOR_RED')), pCity.getX(), pCity.getY(), True, True)
				return True

		return False



	def doReviveActivePlayer(self, argsList):
		"allows you to perform an action after an AIAutoPlay"
		iPlayer = argsList[0]
		return False



	def doPillageGold(self, argsList):
		"controls the gold result of pillaging"
		pPlot = argsList[0]
		pUnit = argsList[1]

		iPillageGold = 0
		iPillageGold = CyGame().getSorenRandNum(gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "Pillage Gold 1")
		iPillageGold += CyGame().getSorenRandNum(gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "Pillage Gold 2")
		iPillageGold += (pUnit.getPillageChange() * iPillageGold) / 100

	### Pillaging - Immunity
		pPlayer = gc.getPlayer(pUnit.getOwner())
		iTrait = HR.Trait.PillageImmunity

		if pPlot.getOwner() > -1:
			pVictim = gc.getPlayer(pPlot.getOwner())
			if pVictim.hasTrait(iTrait):
				pass
				#return 0

	### Pillaging - Improved
		iCivic = HR.Civic.ImprovedPillaging
		iTrait = HR.Trait.ImprovedPillaging
		iPillageBaseGold = iPillageGold

		if pPlayer.hasTrait(iTrait):
			iPillageGold += iPillageBaseGold

		if pPlayer.isCivic(iCivic):
			iPillageGold += iPillageBaseGold
		###

		return iPillageGold



	def doCityCaptureGold(self, argsList):
		"controls the gold result of capturing a city"
		pOldCity = argsList[0]

		iCaptureGold = 0
		iCaptureGold += gc.getDefineINT("BASE_CAPTURE_GOLD")
		iCaptureGold += (pOldCity.getPopulation() * gc.getDefineINT("CAPTURE_GOLD_PER_POPULATION"))
		iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND1"), "Capture Gold 1")
		iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND2"), "Capture Gold 2")

		if gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS") > 0:
			iCaptureGold *= cyIntRange((CyGame().getGameTurn() - pOldCity.getGameTurnAcquired()), 0, gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS"))
			iCaptureGold /= gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS")

		return iCaptureGold



	def citiesDestroyFeatures(self, argsList):
		iX, iY= argsList
		return True



	def canFoundCitiesOnWater(self, argsList):
		iX, iY= argsList
		return False



	def doCombat(self, argsList):
		pSelectionGroup, pDestPlot = argsList
		return False



	def getConscriptUnitType(self, argsList):
		iPlayer = argsList[0]
		iConscriptUnitType = -1 #return this with the value of the UNIT TYPE you want to be conscripted, -1 uses default system
		return iConscriptUnitType



	def getCityFoundValue(self, argsList):
		iPlayer, iPlotX, iPlotY = argsList
		iFoundValue = -1 # Any value besides -1 will be used
		return iFoundValue



	def canPickPlot(self, argsList):
		pPlot = argsList[0]
		return True



	def getUnitCostMod(self, argsList):
		iPlayer, iUnit = argsList
		pPlayer = gc.getPlayer(iPlayer)
		iCostMod = -1

		# Tenets
		iTenet, iModifier = HR_Religion.Tenets().MilitaryUnitCostModifier
		if pPlayer.isCivic(iTenet):
			iCostMod = 100 + iModifier

		return iCostMod



	def getBuildingCostMod(self, argsList):
		iPlayer, iCityID, iBuilding = argsList
		pPlayer = gc.getPlayer(iPlayer)
		pCity = pPlayer.getCity(iCityID)
		iCostMod = 100

		# Capital Building Cost Reduction
		iTrait = HR.Trait.CapitalBuildingModifier[0]
		if pPlayer.hasTrait(iTrait):
			if pCity.isCapital() == False:
				if pPlayer.getCapitalCity().isHasBuilding(iBuilding):
					iCostMod += HR.Trait.CapitalBuildingModifier[1]

		# Cost Change by Advisor
		iStateReligion = pPlayer.getStateReligion()
		if iStateReligion > 0:
			if pCity.isHasReligion(iStateReligion):
				for iTenet, iModifier, iAdvisor in HR_Religion.Tenets().AdvisorBuildingCostModifier:
					if pPlayer.isCivic(iTenet):
						if gc.getBuildingInfo(iBuilding).getAdvisorType() == iAdvisor:
							iCostMod += iModifier

		# Cost Change by Tenet
		iTenet, iModifier = HR_Religion.Tenets().WonderCostModifier
		if pPlayer.isCivic(iTenet):
			iBuildingClass = gc.getBuildingInfo(iBuilding).getBuildingClassType()
			if isNationalWonderClass(iBuildingClass) or isWorldWonderClass(iBuildingClass):
				iCostMod += iModifier

		return iCostMod



	def canUpgradeAnywhere(self, argsList):
		pUnit = argsList
		bCanUpgradeAnywhere = 0
		return bCanUpgradeAnywhere



	def getWidgetHelp(self, argsList):
		'Returns the hover help text for registered widgets, otherwise an empty string'
		eWidgetType, iData1, iData2, bOption = argsList

		# Actions
		if eWidgetType == WidgetTypes.WIDGET_MISSION:
			if iData1 == HR.Mission['MISSION_HUMANITARIAN']:
				pCity = HR.decodeCity(iData2)
				return CivilWar.CivilWar().getHumanitarianMissionHelp(pCity)

			elif iData1 == HR.Mission['MISSION_FOUND_RELIGION']:
				ReligionInfo = gc.getReligionInfo(iData2)
				iTenet = HR_Religion.Tenets().FixedTenets[iData2]
				szHelp = CyTranslator().getText("TXT_KEY_MISSION_FOUND_RELIGION_HELP", (u"%c" % ReligionInfo.getChar(), ReligionInfo.getDescription()))
				szHelp += "\n\n%s" % CyTranslator().changeTextColor(gc.getCivicInfo(iTenet).getDescription(), gc.getInfoTypeForString('COLOR_HIGHLIGHT_TEXT'))
				szHelp += CyGameTextMgr().parseCivicInfo(iTenet, False, False, True)
				return szHelp

			elif iData1 == HR.Mission['MISSION_REFORMATION']:
				ReligionInfo = gc.getReligionInfo(iData2)
				return CyTranslator().getText("TXT_KEY_MISSION_REFORMATION_HELP", (ReligionInfo.getDescription(), ))

			elif iData1 == HR.Mission['MISSION_REPENTANCE']:
				return CyTranslator().getText("TXT_KEY_MISSION_REPENTANCE_HELP", ())

			elif iData1 == HR.Mission['MISSION_GREAT_TEMPLE']:
				szHelp = CyTranslator().getText("TXT_KEY_MISSION_GREAT_TEMPLE_HELP", ())
				szHelp += "\n" + CyGameTextMgr().getBuildingHelp(iData2, False, False, False, None)
				szHelp += "\n\n" + CyTranslator().getText("TXT_KEY_MISSION_CONSTRUCT_HELP", ())
				if szHelp.find("Great Prophet") > - 1:
					szHelp = szHelp.replace(u"%c (Great Prophet)" % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR), u"%c (Great Prophet)" % CyGame().getSymbolID(FontSymbols.RELIGION_CHAR))
				return szHelp

			elif iData1 == HR.Mission['MISSION_INQUISITION']:
				ReligionInfo = gc.getReligionInfo(iData2)
				return CyTranslator().getText('TXT_KEY_MISSION_INQUISITION_HELP', (ReligionInfo.getDescription(), ))

		# Faith Bar
		elif eWidgetType == WidgetTypes.WIDGET_HELP_FAITH_BAR:
			pPlayer = gc.getPlayer(CyGame().getActivePlayer())
			szHelp = HR_Religion.Faith().getFaithBarHelp(pPlayer)
			return szHelp

		# Great General Bar
		elif eWidgetType == WidgetTypes.WIDGET_HELP_GREAT_GENERAL_BAR:
			pPlayer = gc.getPlayer(CyGame().getActivePlayer())
			szHelp = HR.getGreatGeneralBarHelp(pPlayer)
			return szHelp

		# Great Person Bar
		elif eWidgetType == WidgetTypes.WIDGET_HELP_GREAT_PERSON_BAR:
			pPlayer = gc.getPlayer(CyGame().getActivePlayer())
			szHelp = HR.getGreatPersonBarHelp(pPlayer)
			return szHelp

		# Military Advisor
		elif eWidgetType == WidgetTypes.WIDGET_HELP_THREAT_BAR:
			szHelp = ThreatUtil.getThreatHelp(iData1, iData2)
			return szHelp

		elif eWidgetType == WidgetTypes.WIDGET_JUMP_TO_MILITARY_ADVISOR:
			pPlayer = gc.getPlayer(iData1)
			szHelp = CyTranslator().changeTextColor(pPlayer.getName(), gc.getInfoTypeForString('COLOR_HIGHLIGHT_TEXT'))
			szHelp += "\n"
			szHelp += pPlayer.getCivilizationDescription(0)
			szHelp += "\n\n"
			szHelp += CyGameTextMgr().getAttitudeString(iData1, iData2)
			return szHelp

		# Religion Advisor
		elif eWidgetType == WidgetTypes.WIDGET_HELP_RELIGION:
			if iData1 == -1:
				return CyTranslator().getText('TXT_KEY_RELIGION_SCREEN_NO_STATE', ())

		# Tenets Advisor
		elif eWidgetType == WidgetTypes.WIDGET_HELP_TENETS_SCREEN:
			return CyTranslator().getText('TXT_KEY_TENETS_SCREEN_HELP', ())

		# Espionage Advisor
		elif eWidgetType == WidgetTypes.WIDGET_ESPIONAGE_SELECT_PLAYER:
			pPlayer = gc.getPlayer(iData1)
			szHelp = CyTranslator().changeTextColor(pPlayer.getName(), gc.getInfoTypeForString('COLOR_HIGHLIGHT_TEXT'))
			szHelp += "\n"
			szHelp += pPlayer.getCivilizationDescription(0)
			szHelp += "\n\n"
			szHelp += CyGameTextMgr().getAttitudeString(iData1, iData2)
			return szHelp

		elif eWidgetType == WidgetTypes.WIDGET_ESPIONAGE_SELECT_CITY:
			return " "

		elif eWidgetType == WidgetTypes.WIDGET_ESPIONAGE_SELECT_MISSION:
			MissionInfo = gc.getEspionageMissionInfo(iData1)
			szHelp = CyTranslator().changeTextColor(MissionInfo.getDescription(), gc.getInfoTypeForString('COLOR_HIGHLIGHT_TEXT'))
			szHelp += "\n"
			szHelp += MissionInfo.getHelp()
			return szHelp

		# City Screen - Wonder Limits
		elif eWidgetType == WidgetTypes.WIDGET_WONDER_LIMITS:
			szHelp = CyTranslator().changeTextColor(u"World Wonder Limits\n", gc.getInfoTypeForString('COLOR_HIGHLIGHT_TEXT'))
			for iCultureLevel in xrange(gc.getNumCultureLevelInfos()):
				if iCultureLevel > 0:
					iLimit = HR.WorldWonderLimits[iCultureLevel]
					szLevel = gc.getCultureLevelInfo(iCultureLevel).getDescription()
					szHelp += u"%c%d at %s\n" % (CyGame().getSymbolID(FontSymbols.BULLET_CHAR), iLimit, szLevel)

			return szHelp

		# City Screen - Ethnicity Bar
		elif eWidgetType == WidgetTypes.WIDGET_HELP_ETHNICITY_BAR:
			pCity = CyInterface().getHeadSelectedCity()
			if pCity:
				szHelp = HR.getCityEthnicityHelp(pCity)
				return szHelp

		# City Screen - Dissent Bar
		elif eWidgetType == WidgetTypes.WIDGET_HELP_DISSENT_BAR:
			pCity = CyInterface().getHeadSelectedCity()
			if pCity:
				szHelp = CivilWar.CivilWar().getCityDissentHelp(pCity)
				return szHelp

		# City Screen - Great Person Bars
		elif eWidgetType == WidgetTypes.WIDGET_HELP_GREAT_PERSON_CITY_BAR:
			pCity = CyInterface().getHeadSelectedCity()
			if pCity and iData1 > -1:
				szHelp = HR.getGreatPersonCityBarHelp(pCity, iData1)
				return szHelp

		# City Screen - Faith Display
		elif eWidgetType == WidgetTypes.WIDGET_HELP_FAITH_CITY_BAR:
			pCity = CyInterface().getHeadSelectedCity()
			if pCity:
				szHelp = HR_Religion.Faith().getCityFaithBarHelp(pCity)
				return szHelp

		# City Screen - Organization Display
		elif eWidgetType == WidgetTypes.WIDGET_HELP_ORGANIZATION_CITY:
			pCity = CyInterface().getHeadSelectedCity()
			if pCity and iData1 > -1:
				szHelp = HR_Organizations.getOrganizationCityHelp(iData1, pCity)
				return szHelp

		# Tenet Details
		elif eWidgetType == WidgetTypes.WIDGET_PEDIA_JUMP_TO_TENET:
			TenetInfo = gc.getCivicInfo(iData1)
			szHelp = TenetInfo.getDescription()

			if iData1 in HR_Religion.Tenets().TenetTechs.keys():
				iTech = HR_Religion.Tenets().TenetTechs[iData1]
				bTech = False
				iPlayer = CyGame().getActivePlayer()
				if iPlayer > -1:
					if gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isHasTech(iTech):
						bTech = True

				if not bTech:
					szHelp += "\n"
					szHelp += CyTranslator().getText("TXT_KEY_CIVIC_REQUIRES", (gc.getTechInfo(iTech).getDescription(), ))

			szHelp += CyGameTextMgr().parseCivicInfo(iData1, False, False, True)
			return szHelp

		# Organization Details
		elif eWidgetType == WidgetTypes.WIDGET_PEDIA_JUMP_TO_ORGANIZATION or eWidgetType == WidgetTypes.WIDGET_HELP_ORGANIZATION:
			szHelp = HR_Organizations.getOrganizationHelp(iData1, False)
			return szHelp

		# Building Details
		elif eWidgetType == WidgetTypes.WIDGET_PEDIA_JUMP_TO_HR_BUILDING:
			pCity = None
			if iData2 > -1:
				pCity = HR.decodeCity(iData2)

			szHelp = HR.getBuildingHelp(iData1, False, pCity)
			return szHelp

		# Resource Details
		elif eWidgetType == WidgetTypes.WIDGET_PEDIA_JUMP_TO_RESOURCE:
			szHelp = CyGameTextMgr().getBonusHelp(iData1, False)
			szHelp = szHelp.replace("\n+", CyTranslator().getText("[NEWLINE][ICON_BULLET]+", ()))
			iClass = gc.getBonusInfo(iData1).getBonusClassType()
			if iClass in HR_Religion.Tenets().FaithResources.keys():
				iTenet, iChange = HR_Religion.Tenets().FaithResources[iClass]
				szHelp += CyTranslator().getText("TXT_KEY_BONUS_FAITH", (iChange, gc.getCivicInfo(iTenet).getDescription()))

			return szHelp

		# Routes
		elif eWidgetType == WidgetTypes.WIDGET_ROUTE:
			return gc.getRouteInfo(iData1).getDescription()

		# Specialists
		elif eWidgetType == WidgetTypes.WIDGET_HR_CITIZEN:
			szHelp = HR.getSpecialistHelp(iData1)
			return szHelp

		# Go to City
		elif eWidgetType == WidgetTypes.WIDGET_GO_TO_CITY:
			szHelp = "Locate this city in the world"
			return szHelp

		# Technology Advisor
		elif eWidgetType == WidgetTypes.WIDGET_PYTHON:
			if iData1 == 7800:
				return gc.getTechInfo(iData2).getHelp()

			elif iData1 == 7801:
				if iData2 == 0:
					return CyTranslator().getText("TXT_KEY_TECH_SCREEN_FILTER_KNOWN", ())
				elif iData2 == 2:
					return CyTranslator().getText("TXT_KEY_TECH_SCREEN_FILTER_CLAIMED", ())

		# World Builder
			elif iData1 == 1027:
				return CyTranslator().getText("TXT_KEY_WB_PLOT_DATA",())
			elif iData1 == 1028:
				return gc.getGameOptionInfo(iData2).getHelp()
			elif iData1 == 1029:
				if iData2 == 0:
					sText = CyTranslator().getText("TXT_KEY_WB_PYTHON", ())
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onFirstContact"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onChangeWar"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onVassalState"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCityAcquired"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCityBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCultureExpansion"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onGoldenAge"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onEndGoldenAge"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onGreatPersonBorn"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onPlayerChangeStateReligion"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionFounded"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionSpread"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionRemove"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationFounded"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationSpread"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationRemove"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitCreated"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitLost"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitPromoted"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onBuildingBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onProjectBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onTechAcquired"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onImprovementBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onImprovementDestroyed"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onRouteBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onPlotRevealed"
					return sText
				elif iData2 == 1:
					return CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA",())
				elif iData2 == 2:
					return CyTranslator().getText("TXT_KEY_WB_TEAM_DATA",())
				elif iData2 == 3:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH",())
				elif iData2 == 4:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT",())
				elif iData2 == 5:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()) + " + " + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ())
				elif iData2 == 6:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION",())
				elif iData2 == 7:
					return CyTranslator().getText("TXT_KEY_WB_CITY_DATA2",())
				elif iData2 == 8:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING",())
				elif iData2 == 9:
					return "Platy Builder\nVersion: 4.17b"
				elif iData2 == 10:
					return CyTranslator().getText("TXT_KEY_CONCEPT_EVENTS",())
				elif iData2 == 11:
					return CyTranslator().getText("TXT_KEY_WB_RIVER_PLACEMENT",())
				elif iData2 == 12:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT",())
				elif iData2 == 13:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS",())
				elif iData2 == 14:
					return CyTranslator().getText("TXT_KEY_WB_PLOT_TYPE",())
				elif iData2 == 15:
					return CyTranslator().getText("TXT_KEY_CONCEPT_TERRAIN",())
				elif iData2 == 16:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_ROUTE",())
				elif iData2 == 17:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_FEATURE",())
				elif iData2 == 18:
					return CyTranslator().getText("TXT_KEY_MISSION_BUILD_CITY",())
				elif iData2 == 19:
					return CyTranslator().getText("TXT_KEY_WB_ADD_BUILDINGS",())
				elif iData2 == 20:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION",())
				elif iData2 == 21:
					return CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS",())
				elif iData2 == 22:
					return CyTranslator().getText("TXT_KEY_ESPIONAGE_CULTURE",())
				elif iData2 == 23:
					return CyTranslator().getText("TXT_KEY_PITBOSS_GAME_OPTIONS",())
				elif iData2 == 24:
					return CyTranslator().getText("TXT_KEY_WB_SENSIBILITY",())
				elif iData2 == 27:
					return CyTranslator().getText("TXT_KEY_WB_ADD_UNITS",())
				elif iData2 == 28:
					return CyTranslator().getText("TXT_KEY_WB_TERRITORY",())
				elif iData2 == 29:
					return CyTranslator().getText("TXT_KEY_WB_ERASE_ALL_PLOTS",())
				elif iData2 == 30:
					return CyTranslator().getText("TXT_KEY_WB_REPEATABLE",())
				elif iData2 == 31:
					return CyTranslator().getText("TXT_KEY_PEDIA_HIDE_INACTIVE", ())
				elif iData2 == 32:
					return CyTranslator().getText("TXT_KEY_WB_STARTING_PLOT", ())
				elif iData2 == 33:
					return CyTranslator().getText("TXT_KEY_INFO_SCREEN", ())
				elif iData2 == 34:
					return CyTranslator().getText("TXT_KEY_CONCEPT_TRADE", ())
			elif iData1 > 1029 and iData1 < 1040:
				if iData1 %2:
					return "-"
				return "+"
			elif iData1 == 1041:
				return CyTranslator().getText("TXT_KEY_WB_KILL",())
			elif iData1 == 1042:
				return CyTranslator().getText("TXT_KEY_MISSION_SKIP",())
			elif iData1 == 1043:
				if iData2 == 0:
					return CyTranslator().getText("TXT_KEY_WB_DONE",())
				elif iData2 == 1:
					return CyTranslator().getText("TXT_KEY_WB_FORTIFY",())
				elif iData2 == 2:
					return CyTranslator().getText("TXT_KEY_WB_WAIT",())
			elif iData1 == 6782:
				return CyGameTextMgr().parseCorporationInfo(iData2, False)
			elif iData1 == 6785:
				return CyGameTextMgr().getProjectHelp(iData2, False, CyCity())
			elif iData1 == 6787:
				return gc.getProcessInfo(iData2).getDescription()
			elif iData1 == 6788:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return gc.getRouteInfo(iData2).getDescription()
			elif iData1 > 7199 and iData1 < 7300:
				iPlayer = iData1 - 7200
				pPlayer = gc.getPlayer(iPlayer)
				pCity = pPlayer.getCity(iData2)
				if CyGame().GetWorldBuilderMode():
					sText = "<font=3>"
					if pCity.isCapital():
						sText += CyTranslator().getText("[ICON_STAR]", ())
					elif pCity.isGovernmentCenter():
						sText += CyTranslator().getText("[ICON_SILVER_STAR]", ())
					sText += u"%s: %d<font=2>" %(pCity.getName(), pCity.getPopulation())
					sTemp = ""
					if pCity.isConnectedToCapital(iPlayer):
						sTemp += CyTranslator().getText("[ICON_TRADE]", ())
					for i in xrange(gc.getNumReligionInfos()):
						if pCity.isHolyCityByType(i):
							sTemp += u"%c" %(gc.getReligionInfo(i).getHolyCityChar())
						elif pCity.isHasReligion(i):
							sTemp += u"%c" %(gc.getReligionInfo(i).getChar())

					for i in xrange(gc.getNumCorporationInfos()):
						if pCity.isHeadquartersByType(i):
							sTemp += u"%c" %(gc.getCorporationInfo(i).getHeadquarterChar())
						elif pCity.isHasCorporation(i):
							sTemp += u"%c" %(gc.getCorporationInfo(i).getChar())
					if len(sTemp) > 0:
						sText += "\n" + sTemp

					iMaxDefense = pCity.getTotalDefense(False)
					if iMaxDefense > 0:
						sText += u"\n%s: " %(CyTranslator().getText("[ICON_DEFENSE]", ()))
						iCurrent = pCity.getDefenseModifier(False)
						if iCurrent != iMaxDefense:
							sText += u"%d/" %(iCurrent)
						sText += u"%d%%" %(iMaxDefense)

					sText += u"\n%s: %d/%d" %(CyTranslator().getText("[ICON_FOOD]", ()), pCity.getFood(), pCity.growthThreshold())
					iFoodGrowth = pCity.foodDifference(True)
					if iFoodGrowth != 0:
						sText += u" %+d" %(iFoodGrowth)

					if pCity.isProduction():
						sText += u"\n%s:" %(CyTranslator().getText("[ICON_PRODUCTION]", ()))
						if not pCity.isProductionProcess():
							sText += u" %d/%d" %(pCity.getProduction(), pCity.getProductionNeeded())
							iProduction = pCity.getCurrentProductionDifference(False, True)
							if iProduction != 0:
								sText += u" %+d" %(iProduction)
						sText += u" (%s)" %(pCity.getProductionName())

					iGPRate = pCity.getGreatPeopleRate()
					iProgress = pCity.getGreatPeopleProgress()
					if iGPRate > 0 or iProgress > 0:
						sText += u"\n%s: %d/%d %+d" %(CyTranslator().getText("[ICON_GREATPEOPLE]", ()), iProgress, pPlayer.greatPeopleThreshold(False), iGPRate)

					sText += u"\n%s: %d/%d (%s)" %(CyTranslator().getText("[ICON_CULTURE]", ()), pCity.getCulture(iPlayer), pCity.getCultureThreshold(), gc.getCultureLevelInfo(pCity.getCultureLevel()).getDescription())

					lTemp = []
					for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
						iAmount = pCity.getCommerceRateTimes100(i)
						if iAmount <= 0: continue
						sTemp = u"%d.%02d%c" %(pCity.getCommerceRate(i), pCity.getCommerceRateTimes100(i)%100, gc.getCommerceInfo(i).getChar())
						lTemp.append(sTemp)
					if len(lTemp) > 0:
						sText += "\n"
						for i in xrange(len(lTemp)):
							sText += lTemp[i]
							if i < len(lTemp) - 1:
								sText += ", "

					iMaintenance = pCity.getMaintenanceTimes100()
					if iMaintenance != 0:
						sText += "\n" + CyTranslator().getText("[COLOR_WARNING_TEXT]", ()) + CyTranslator().getText("INTERFACE_CITY_MAINTENANCE", ()) + " </color>"
						sText += u"-%d.%02d%c" %(iMaintenance/100, iMaintenance%100, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())

					lBuildings = []
					lWonders = []
					for i in xrange(gc.getNumBuildingInfos()):
						if pCity.isHasBuilding(i):
							Info = gc.getBuildingInfo(i)
							if isLimitedWonderClass(Info.getBuildingClassType()):
								lWonders.append(Info.getDescription())
							else:
								lBuildings.append(Info.getDescription())
					if len(lBuildings) > 0:
						lBuildings.sort()
						sText += "\n" + CyTranslator().getText("[COLOR_BUILDING_TEXT]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()) + ": </color>"
						for i in xrange(len(lBuildings)):
							sText += lBuildings[i]
							if i < len(lBuildings) - 1:
								sText += ", "
					if len(lWonders) > 0:
						lWonders.sort()
						sText += "\n" + CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS", ()) + ": </color>"
						for i in xrange(len(lWonders)):
							sText += lWonders[i]
							if i < len(lWonders) - 1:
								sText += ", "
					sText += "</font>"
					return sText
			elif iData1 == 7869:
				return CyGameTextMgr().parseReligionInfo(iData2, False)
			elif iData1 == 7870:
				return CyGameTextMgr().getBuildingHelp(iData2, False, False, False, None)
			elif iData1 == 7871:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return CyGameTextMgr().getTechHelp(iData2, False, False, False, False, -1)
			elif iData1 == 7872:
				iCiv = iData2 % 10000
				return CyGameTextMgr().parseCivInfos(iCiv, False)
			elif iData1 == 7873:
				return CyGameTextMgr().getPromotionHelp(iData2, False)
			elif iData1 == 7874:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				iFeature = iData2 % 10000
				return CyGameTextMgr().getFeatureHelp(iFeature, False)
			elif iData1 == 7875:
				return CyGameTextMgr().getTerrainHelp(iData2, False)
			elif iData1 == 7876:
				iLeader = iData2 % 10000
				return CyGameTextMgr().parseLeaderTraits(iLeader, -1, False, False)
			elif iData1 == 7877:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return CyGameTextMgr().getImprovementHelp(iData2, False)
			elif iData1 == 7878:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return CyGameTextMgr().getBonusHelp(iData2, False)
			elif iData1 == 7879:
				return CyGameTextMgr().getSpecialistHelp(iData2, False)
			elif iData1 == 7880:
				return gc.getYieldInfo(iData2).getDescription()
			elif iData1 == 7881:
				return gc.getCommerceInfo(iData2).getDescription()
			elif iData1 == 7882:
				return gc.getBuildInfo(iData2).getDescription()
			elif iData1 == 8201:
				return CyGameTextMgr().parseCorporationInfo(iData2, False)
			elif iData1 == 8202:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_PEDIA_ALL_UNITS", ())
				return CyGameTextMgr().getUnitHelp(iData2, False, False, False, None)
			elif iData1 > 8299 and iData1 < 8400:
				iPlayer = iData1 - 8300
				pUnit = gc.getPlayer(iPlayer).getUnit(iData2)
				sText = CyGameTextMgr().getSpecificUnitHelp(pUnit, True, False)
				if CyGame().GetWorldBuilderMode():
					sText += "\n" + CyTranslator().getText("TXT_KEY_WB_UNIT", ()) + " ID: " + str(iData2)
					sText += "\n" + CyTranslator().getText("TXT_KEY_WB_GROUP", ()) + " ID: " + str(pUnit.getGroupID())
					sText += "\n" + "X: " + str(pUnit.getX()) + ", Y: " + str(pUnit.getY())
					sText += "\n" + CyTranslator().getText("TXT_KEY_WB_AREA_ID", ()) + ": "  + str(pUnit.plot().getArea())
				return sText
			elif iData1 == 8205 or iData1 == 8206:
				sText = CyGameTextMgr().parseCivicInfo(iData2, False, True, False)
				if gc.getCivicInfo(iData2).getUpkeep() > -1:
					sText += "\n" + gc.getUpkeepInfo(gc.getCivicInfo(iData2).getUpkeep()).getDescription()
				else:
					sText += "\n" + CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())
				return sText

		# BUG
		func = WidgetUtil.g_widgetHelp.get(eWidgetType)
		if func:
			return func(eWidgetType, iData1, iData2, bOption)

		return u""



	def getUpgradePriceOverride(self, argsList):
		iPlayer, iUnitID, iUnitTypeUpgrade = argsList

	### Cheaper Upgrades
		pPlayer = gc.getPlayer(iPlayer)
		pUnit = pPlayer.getUnit(iUnitID)
		iTrait, iTraitDiscount = HR.Trait.MilitaryUnitUpgradeDiscount

		iDiscount = pUnit.getUpgradeDiscount()
		iPrice = gc.getDefineINT("BASE_UNIT_UPGRADE_COST")
		iPrice += (max(0, (pPlayer.getUnitProductionNeeded(iUnitTypeUpgrade) - pPlayer.getUnitProductionNeeded(pUnit.getUnitType()))) * gc.getDefineINT("UNIT_UPGRADE_COST_PER_PRODUCTION"))

		if not pPlayer.isHuman() and not pPlayer.isBarbarian():
			pHandicapInfo = gc.getHandicapInfo(CyGame().getHandicapType())
			iPrice *= pHandicapInfo.getAIUnitUpgradePercent() / 100
			iPrice *= max(0, ((pHandicapInfo.getAIPerEraModifier() * pPlayer.getCurrentEra()) + 100)) / 100

		# Exclude non-military units from discounts
		if pUnit.getUnitCombatType() > -1:
			if pPlayer.hasTrait(iTrait):
				iDiscount -= iTraitDiscount

		iPrice = iPrice * (100 - iDiscount) / 100
		return max(0, iPrice)



	def getExperienceNeeded(self, argsList):
		iLevel, iOwner = argsList
		iExperienceNeeded = 0

		# Regular epic game experience
		iExperienceNeeded = iLevel * iLevel + 1
		iModifier = gc.getPlayer(iOwner).getLevelExperienceModifier()
		if iModifier != 0:
			iExperienceNeeded += (iExperienceNeeded * iModifier + 99) / 100   # ROUND UP

		return iExperienceNeeded
