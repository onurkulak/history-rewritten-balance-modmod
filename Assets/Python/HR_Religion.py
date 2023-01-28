from CvPythonExtensions import *
import CvEventManager
import CvScreensInterface
import HR
import HR_Map
import HR_Religion
import CivilWar

gc = CyGlobalContext()

NumTemplesRequiredForGreatTemple	= 4		# Scales with WorldSize
NumTemplesRequiredForMonastery		= 2 	# Scales with WorldSize



def foundReligion(iReligion, pPlayer, pCity):
	'Founds specified religion in specified city'
	CyGame().setHolyCity(iReligion, pCity, True)
	ReligionInfo = gc.getReligionInfo(iReligion)
	iMissionaryClass = ReligionInfo.getFreeUnitClass()
	if iMissionaryClass > -1:
		iMissionary = gc.getCivilizationInfo(pCity.getCivilizationType()).getCivilizationUnits(iMissionaryClass)
		for i in xrange(ReligionInfo.getNumFreeUnits()):
			pNewUnit = pPlayer.initUnit(iMissionary, pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.NO_DIRECTION)



def chooseReligion(pPlayer, pCity):
	'Chooses a religion for the player to found'
	iFavReligion = gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteReligion()
	if iFavReligion > -1:
		if not CyGame().isReligionFounded(iFavReligion):
			return iFavReligion

	lReligion = []
	for iReligion in xrange(gc.getNumReligionInfos()):
		if not CyGame().isReligionFounded(iReligion):
			lReligion.append(iReligion)

	if len(lReligion) > 0:
		iReligion = lReligion[CyGame().getSorenRandNum(len(lReligion), "Chosen Religion")]
		return iReligion

	return -1



def adoptReligion(pPlayer, iOldReligion, iNewReligion):
	'Applies tenet changes when a player adopts a new state religion'

	# Tenet Changes
	if iNewReligion > -1:
		iFaithLeader = Faith().getHighestFaithPlayer(iNewReligion, pPlayer.getID())
		if iFaithLeader > -1 and iFaithLeader != pPlayer.getID():
			for iCategory in xrange(gc.getNumCivicOptionInfos()):
				if Tenets().isTenetCategory(iCategory):
					iTenet = gc.getPlayer(iFaithLeader).getCivics(iCategory)
					pPlayer.setCivics(iCategory, iTenet)

		else:
			if iNewReligion in Tenets().FixedTenets:
				iFixedTenet = Tenets().FixedTenets[iNewReligion]
				iFixedCategory = gc.getCivicInfo(iFixedTenet).getCivicOptionType()
				pPlayer.setCivics(iFixedCategory, iFixedTenet)

			Tenets().callReformation(pPlayer, [])

	# Religious Buildings
	iOldTemple = -1
	iOldGreatTemple = -1
	iOldMonastery = -1
	iNewTemple = -1
	iNewGreatTemple = -1
	iNewMonastery = -1

	if iOldReligion > -1:
		iOldTemple = getReligionTemple(iOldReligion)
		iOldGreatTemple = getReligionGreatTemple(iOldReligion)
		iOldMonastery = getReligionMonastery(iOldReligion)

	if iNewReligion > -1:
		iNewTemple = getReligionTemple(iNewReligion)
		iNewGreatTemple = getReligionGreatTemple(iNewReligion)
		iNewMonastery = getReligionMonastery(iNewReligion)

	iHappyTenet, iHappyChange = Tenets().TempleHappiness
	iHealthTenet, iHealthChange = Tenets().TempleHealth
	iTradeRouteTenet, iTradeRoutes = Tenets().MonasteryTradeRoutes

	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		if iOldTemple > -1:
			iOldTempleClass = gc.getBuildingInfo(iOldTemple).getBuildingClassType()
			for iYieldTenet in Tenets().TempleYield.keys():
				if pPlayer.isCivic(iYieldTenet):
					iYieldType, iYieldChange = Tenets().TempleYield[iYieldTenet]
					loopCity.setBuildingYieldChange(iOldTempleClass, iYieldType, 0)
			if loopCity.getNumBuilding(iOldTemple) > 0:
				if pPlayer.isCivic(iHappyTenet):
					loopCity.changeExtraHappiness(-iHappyChange)
				if pPlayer.isCivic(iHealthTenet):
					loopCity.changeExtraHealth(-iHealthChange)

		if iNewTemple > -1:
			iNewTempleClass = gc.getBuildingInfo(iNewTemple).getBuildingClassType()
			for iYieldTenet in Tenets().TempleYield.keys():
				if pPlayer.isCivic(iYieldTenet):
					iYieldType, iYieldChange = Tenets().TempleYield[iYieldTenet]
					loopCity.setBuildingYieldChange(iNewTempleClass, iYieldType, iYieldChange)
			if loopCity.getNumBuilding(iNewTemple) > 0:
				if pPlayer.isCivic(iHappyTenet):
					loopCity.changeExtraHappiness(iHappyChange)
				if pPlayer.isCivic(iHealthTenet):
					loopCity.changeExtraHealth(iHealthChange)

		if iOldGreatTemple > -1:
			for iTenet, iSpecialist in Tenets().GreatTempleSpecialist.items():
				if pPlayer.isCivic(iYieldTenet):
					if loopCity.getNumBuilding(iOldGreatTemple) > 0:
						loopCity.changeFreeSpecialistCount(iSpecialist, -1)

		if iNewGreatTemple > -1:
			for iTenet, iSpecialist in Tenets().GreatTempleSpecialist.items():
				if pPlayer.isCivic(iYieldTenet):
					if loopCity.getNumBuilding(iNewGreatTemple) > 0:
						loopCity.changeFreeSpecialistCount(iSpecialist, 1)

		if iOldMonastery > -1:
			if loopCity.getNumBuilding(iOldMonastery) > 0:
				if pPlayer.isCivic(iTradeRouteTenet):
						pCity.changeExtraTradeRoutes(-iTradeRoutes)

		if iNewMonastery > -1:
			if loopCity.getNumBuilding(iNewMonastery) > 0:
				if pPlayer.isCivic(iTradeRouteTenet):
						pCity.changeExtraTradeRoutes(iTradeRoutes)

		(loopCity, iter) = pPlayer.nextCity(iter, False)



def getNumReligionsFounded():
	''
	iReligionCount = 0
	for iReligion in xrange(gc.getNumReligionInfos()):
		if CyGame().isReligionFounded(iReligion):
			iReligionCount += 1

	return iReligionCount



def getReligionLimit():
	'Returns the maximum number of religions that can be founded in this game'
	iMaxReligions = min(gc.getGame().countCivPlayersEverAlive(), 18)
	if CyGame().isOption(GameOptionTypes.GAMEOPTION_PICK_RELIGION):
		iMaxReligions *= 2
		iMaxReligions /= 3

	return iMaxReligions



def getReligionTemple(iReligion):
	''
	iBuilding = -1
	if iReligion > -1:
		sType = gc.getReligionInfo(iReligion).getType().replace("RELIGION_", "BUILDING_TEMPLE_")
		iBuilding = gc.getInfoTypeForString(sType)

	return iBuilding



def getReligionGreatTemple(iReligion):
	''
	iBuilding = -1
	if iReligion > -1:
		sType = gc.getReligionInfo(iReligion).getType().replace("RELIGION_", "BUILDING_GREAT_TEMPLE_")
		iBuilding = gc.getInfoTypeForString(sType)

	return iBuilding



def getReligionMonastery(iReligion):
	''
	iBuilding = -1
	if iReligion > -1:
		sType = gc.getReligionInfo(iReligion).getType().replace("RELIGION_", "BUILDING_MONASTERY_")
		iBuilding = gc.getInfoTypeForString(sType)

	return iBuilding



def getReligionShrine(iReligion):
	''
	iBuilding = -1
	if iReligion > -1:
		sType = gc.getReligionInfo(iReligion).getType().replace("RELIGION_", "BUILDING_SHRINE_")
		iBuilding = gc.getInfoTypeForString(sType)

	return iBuilding



def getMaxReligiousUnit():
	''
	iMax = max(2, int(CyMap().getWorldSize()))
	return iMax



def getReligiousAttitude(pJudge, pAccused, bOldTenets):
	'Returns the religious attitude the first player has towards the second'
	if pJudge.isHuman() or pJudge.getStateReligion() == -1:
		iAttitudeChange = 0

	else:
		iPositiveChange = 0
		iNegativeChange = 0

		TenetList = Tenets().getTenetData(pAccused)
		for i in xrange(len(TenetList)):
			iCategory = i + len(HR.getCivicData(pAccused))
			if iCategory != gc.getInfoTypeForString('CIVICOPTION_TENET_TOLERANCE'):
				if bOldTenets:
					iTenet = TenetList[i]
				else:
					iTenet = pAccused.getCivics(iCategory)

				if pJudge.isCivic(iTenet):
					iPositiveChange += 1
				else:
					iNegativeChange += 1

		if iPositiveChange > 0:
			iSimilarityTenet, iSimilarityModifier = Tenets().ReligiousSimilarityModifier
			if pAccused.isCivic(iSimilarityTenet):
				iPositiveChange += max(1, (iPositiveChange * iSimilarityModifier / 100))

		elif iNegativeChange > 0:
			iDifferenceTenet, iDifferenceModifier = Tenets().ReligiousDifferenceModifier
			if pAccused.isCivic(iDifferenceTenet):
				iNegativeChange += min(-1, (iNegativeChange * iDifferenceModifier / 100))

		iAttitudeChange = iPositiveChange - iNegativeChange

		iApostasyTenet, iApostasyAttitudeChange = Tenets().ApostasyAttitudeChange
		if pAccused.isCivic(iApostasyTenet):
			iAttitudeChange += iApostasyAttitudeChange

	return iAttitudeChange



def setReligiousAttitude(pPlayer):
	''
	for iRival in xrange(gc.getMAX_CIV_PLAYERS()):
		pRival = gc.getPlayer(iRival)
		if pRival.isAlive() and iRival != pPlayer.getID():
			if not pPlayer.isHuman():
				iAttitudeChange = getReligiousAttitude(pPlayer, pRival, True)
				pPlayer.AI_changeAttitudeExtra(iRival, -iAttitudeChange)
				iAttitudeChange = getReligiousAttitude(pPlayer, pRival, False)
				pPlayer.AI_changeAttitudeExtra(iRival, iAttitudeChange)
			if not pRival.isHuman():
				iAttitudeChange = getReligiousAttitude(pRival, pPlayer, True)
				pRival.AI_changeAttitudeExtra(pPlayer.getID(), -iAttitudeChange)
				iAttitudeChange = getReligiousAttitude(pRival, pPlayer, False)
				pRival.AI_changeAttitudeExtra(pPlayer.getID(), iAttitudeChange)



def doProphetAI(pPlayer, pCity, pUnit):
	''
	iStateReligion = pPlayer.getStateReligion()

	# Found Religion
	if not pCity.isHolyCity():
		iReligionCount = 0
		for iReligion in xrange(gc.getNumReligionInfos()):
			if CyGame().isReligionFounded(iReligion):
				iReligionCount += 1

		if iReligionCount < getReligionLimit():
			iChance = 100
			if iStateReligion > -1:
				iChance -= 25
			iChance -= pPlayer.countHolyCities() * 25
			iChance = max(10, iChance)
			if CyGame().getSorenRandNum(100, "Found Religion") < iChance:
				iReligion = chooseReligion(pPlayer, pCity)
				if iReligion > -1:
					foundReligion(iReligion, pPlayer, pCity)
					pUnit.kill(False, -1)
					return True

	# Construct Great Temple (State Religion)
	if canConstructGreatTemple(pCity, iStateReligion):
		iBuilding = getReligionGreatTemple(iStateReligion)
		pCity.setNumRealBuilding(iBuilding, 1)
		CvEventManager.CvEventManager().onBuildingBuilt((pCity, iBuilding))
		pUnit.kill(False, -1)
		return True

	# Reformation
	if Tenets().canReformation(pPlayer):
		iChance = 0
		TenetList = Tenets().selectAITenets(pPlayer, iStateReligion)
		for iTenet in TenetList:
			if iTenet != pPlayer.getCivics(TenetList.index(iTenet)):
				iChance += 25

		if CyGame().getSorenRandNum(100, "Chance of Reformation") < iChance:
			Tenets().callReformation(pPlayer, TenetList)
			pUnit.kill(False, -1)
			return True

	# Repentance
	elif Tenets().canRepentance(pPlayer):
		if not Tenets().AllowRepentance in Tenets().getLovedTenets(pPlayer.getLeaderType()):
			iChance = pPlayer.countHolyCities() * 25
			for iFlavor in Tenets().getTenetBadFlavors(Tenets().AllowRepentance):
				iChance += 10 *	gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFlavorValue(iFlavor)

			if CyGame().getSorenRandNum(100, "Chance of Repentance") < iChance:
				Tenets().doRepentance(pPlayer)
				pUnit.kill(False, -1)
				return True

	# Construct Great Temple (Other Religions)
	if pPlayer.getNonStateReligionHappiness() > 0:
		for iReligion in xrange(gc.getNumReligionInfos()):
			GreatTempleList = []
			if canConstructGreatTemple(pCity, iReligion):
				iBuilding = getReligionGreatTemple(iReligion)
				GreatTempleList.append(iBuilding)

		if GreatTempleList != []:
			iBuilding = GreatTempleList[CyGame().getSorenRandNum(len(GreatTempleList), "AI: Choose Great Temple")]
			pCity.setNumRealBuilding(iBuilding, 1)
			CvEventManager.CvEventManager().onBuildingBuilt((pCity, iBuilding))
			pUnit.kill(False, -1)
			return True

	return False



def canConstructGreatTemple(pCity, iReligion):
	'Returns true if player has enough Temples to construct a new Great Temple in this city'
	iGreatTemple = getReligionGreatTemple(iReligion)

	if pCity.canConstruct(iGreatTemple, False, False, True):
		if CyGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE):
			return True

		pPlayer = gc.getPlayer(pCity.getOwner())
		iBaseReq = NumTemplesRequiredForGreatTemple

		nTemple = pPlayer.countNumBuildings(getReligionTemple(iReligion))
		nGreatTemple = pPlayer.countNumBuildings(iGreatTemple)
		nRequired = iBaseReq + (iBaseReq * gc.getWorldInfo(CyMap().getWorldSize()).getBuildingClassPrereqModifier() / 100)

		iTenet, iChange = Tenets().ChangeGreatTempleRequirement
		if pPlayer.isCivic(iTenet):
			nRequired += iChange

		if nTemple - (nGreatTemple * nRequired) >= nRequired:
			return True

	return False



def canConstructMonastery(pCity, iReligion):
	'Returns true if player has enough Temples to construct a new Monastery in this city'
	if CyGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE):
		return True

	pPlayer = gc.getPlayer(pCity.getOwner())
	iMonastery = getReligionMonastery(iReligion)
	iBaseReq = NumTemplesRequiredForMonastery

	nTemple = pPlayer.countNumBuildings(getReligionTemple(iReligion))
	nMonastery = pPlayer.countNumBuildings(iMonastery)
	nRequired = iBaseReq + (iBaseReq * gc.getWorldInfo(CyMap().getWorldSize()).getBuildingClassPrereqModifier() / 100)

	iTenet, iChange = Tenets().ChangeMonasteryRequirement
	if pPlayer.isCivic(iTenet):
		nRequired += iChange

	if nTemple - (nMonastery * nRequired) >= nRequired:
		return True

	return False



class Faith:
	def __init__(self):
		self.iThresholdIncrease = 250 * 50 * (CyGame().getGameSpeedType() + 1) / 100



	def doFaith(self, pPlayer):
		''
		if not pPlayer.isAnarchy():
			iFaith = self.getFaith(pPlayer)
			iFaith += self.getFaithRate(pPlayer)
			self.setFaith(pPlayer, iFaith)



	def getFaith(self, pPlayer):
		''
		FaithData = HR.getPlayerData(pPlayer, HR.PlayerData.index('FAITH')).split("/")
		iFaith = int(FaithData[0])
		return iFaith



	def setFaith(self, pPlayer, iFaith):
		''
		FaithData = HR.getPlayerData(pPlayer, HR.PlayerData.index('FAITH')).split("/")
		iThreshold = int(FaithData[1])

		if iFaith >= iThreshold:
			self.increaseFaithThreshold(pPlayer)

		else:
			newFaithData = str(iFaith) + "/" + str(iThreshold)
			HR.setPlayerData(pPlayer, HR.PlayerData.index('FAITH'), newFaithData)



	def changeFaith(self, pPlayer, iChange):
		''
		FaithData = HR.getPlayerData(pPlayer, HR.PlayerData.index('FAITH')).split("/")
		iFaith = int(FaithData[0]) + iChange
		iThreshold = int(FaithData[1])

		if iFaith >= iThreshold:
			self.increaseFaithThreshold(pPlayer)

		else:
			newFaithData = str(iFaith) + "/" + str(iThreshold)
			HR.setPlayerData(pPlayer, HR.PlayerData.index('FAITH'), newFaithData)



	def getFaithRate(self, pPlayer):
		'Returns the faith a player generates each turn'
		iFaith = 0

		(loopCity, iter) = pPlayer.firstCity(False)
		while(loopCity):
			iFaith += self.getCityFaithRate(loopCity, False)
			(loopCity, iter) = pPlayer.nextCity(iter, False)

		iFaith += self.getFaithFromForeignBuildings(pPlayer)
		iFaith += self.getFaithFromResources(pPlayer)
		iFaith += (iFaith * self.getFaithModifier(pPlayer) / 100)

		return iFaith



	def getCityFaithRate(self, pCity, bModified):
		'Returns the faith a city generates each turn'
		iFaith = 0
		iFaith += self.getFaithFromBuildings(pCity, True, True, True)
		iFaith += self.getFaithFromSpecialists(pCity)

		if bModified:
			pPlayer = gc.getPlayer(pCity.getOwner())
			iFaith += (iFaith * self.getFaithModifier(pPlayer) / 100)

		return iFaith



	def getFaithFromBuildings(self, pCity, bIncludeBuildings, bIncludeWonders, bIncludeNonState):
		''
		pPlayer = gc.getPlayer(pCity.getOwner())

		iFaith = 0
		iBuildingTotal = 0
		iWonderTotal = 0
		iNonStateTotal = 0

		iWonderTenet, iWonderFaith = Tenets().WonderFaith
		for iBuildingClass in xrange(gc.getNumBuildingClassInfos()):
			iBuilding = HR.getPlayerBuilding(pPlayer, iBuildingClass)
			if iBuilding > -1:
				if pCity.getNumBuilding(iBuilding) == 0:
					continue

				bWonder = False
				BuildingInfo = gc.getBuildingInfo(iBuilding)
				if HR.getBuildingCategory(iBuilding) in (3, 4, 5, 6, 7):
					bWonder = True
					if pPlayer.isCivic(iWonderTenet):
						iWonderTotal += iWonderFaith

				if BuildingInfo.getGreatPeopleUnitClass() == gc.getInfoTypeForString('UNITCLASS_PROPHET'):
					iBuildingReligion = BuildingInfo.getPrereqReligion()
					if iBuildingReligion == -1 or iBuildingReligion == pPlayer.getStateReligion():
						if bWonder:
							iWonderTotal += BuildingInfo.getGreatPeopleRateChange()
						else:
							iBuildingTotal += BuildingInfo.getGreatPeopleRateChange()

					else:
						iNonStateTotal += BuildingInfo.getGreatPeopleRateChange()

		if bIncludeBuildings:
			iFaith += iBuildingTotal

		if bIncludeWonders:
			iFaith += iWonderTotal

		if bIncludeNonState:
			iTenet, iPercent = Tenets().NonStateBuildingFaith
			if pPlayer.isCivic(iTenet):
				iFaith += (iNonStateTotal * iPercent / 100)

		return iFaith



	def getFaithFromForeignBuildings(self, pPlayer):
		''
		iFaith = 0

		iTenet, iPercent = Tenets().ForeignBuildingFaith
		if pPlayer.isCivic(iTenet):
			for iPlayer in xrange(gc.getMAX_PLAYERS()):
				if iPlayer == pPlayer.getID():
					continue

				iRivalFaith = 0
				loopPlayer = gc.getPlayer(iPlayer)
				for iBuildingClass in xrange(gc.getNumBuildingClassInfos()):
					iCount = loopPlayer.getBuildingClassCount(iBuildingClass)
					if iCount == 0:
						continue

					iBuilding = HR.getPlayerBuilding(loopPlayer, iBuildingClass)
					if iBuilding > -1:
						BuildingInfo = gc.getBuildingInfo(iBuilding)
						if BuildingInfo.getGreatPeopleUnitClass() == gc.getInfoTypeForString('UNITCLASS_PROPHET'):
							iBuildingReligion = BuildingInfo.getPrereqReligion()
							if iBuildingReligion > -1:
								if iBuildingReligion == pPlayer.getStateReligion():
									iRivalFaith += (iCount * BuildingInfo.getGreatPeopleRateChange())

				iFaith += (iRivalFaith * iPercent / 100)

		return iFaith



	def getFaithFromResources(self, pPlayer):
		''
		iFaith = 0

		for iResource in xrange(gc.getNumBonusInfos()):
			iClass = gc.getBonusInfo(iResource).getBonusClassType()
			if iClass in Tenets().FaithResources.keys():
				iTenet, iChange = Tenets().FaithResources[iClass]
				if pPlayer.isCivic(iTenet):
					iFaith += (pPlayer.getNumAvailableBonuses(iResource) * iChange)

		return iFaith



	def getFaithFromSpecialists(self, pCity):
		''
		pPlayer = gc.getPlayer(pCity.getOwner())
		iFaith = 0

		iGreatSpecialistTenet, iGreatSpecialistFaith = Tenets().GreatSpecialistFaith
		for iSpecialist in xrange(gc.getNumSpecialistInfos()):
			SpecialistInfo = gc.getSpecialistInfo(iSpecialist)
			if SpecialistInfo.getGreatPeopleUnitClass() == gc.getInfoTypeForString('UNITCLASS_PROPHET'):
				iCount = pCity.getSpecialistCount(iSpecialist) + pCity.getFreeSpecialistCount(iSpecialist)
				iFaith += (SpecialistInfo.getGreatPeopleRateChange() * iCount)

			if pPlayer.isCivic(iGreatSpecialistTenet):
				if iSpecialist in HR.GreatSpecialist:
					iCount = pCity.getSpecialistCount(iSpecialist) + pCity.getFreeSpecialistCount(iSpecialist)
					iFaith += (iGreatSpecialistFaith * iCount)

		return iFaith



	def getFaithModifier(self, pPlayer):
		''
		iModifier = 0

		# Trait
		iUnit = gc.getInfoTypeForString('UNIT_PROPHET')
		if iUnit in HR.Trait.GreatPersonTypeModifier.keys():
			iTrait, iTraitModifier = HR.Trait.GreatPersonTypeModifier[iUnit]
			if pPlayer.hasTrait(iTrait):
				iModifier += iTraitModifier

		# Golden Age
		iGoldenAgeTenet, iGoldenAgeModifier = Tenets().GoldenAgeFaithModifier
		if pPlayer.isCivic(iGoldenAgeTenet):
			if pPlayer.isGoldenAge():
				iModifier += iGoldenAgeModifier

		return iModifier



	def getFaithThreshold(self, pPlayer):
		''
		FaithData = HR.getPlayerData(pPlayer, HR.PlayerData.index('FAITH')).split("/")
		iFaithThreshold = int(FaithData[1])
		return iFaithThreshold



	def setFaithThreshold(self, pPlayer, iThreshold):
		''
		FaithData = HR.getPlayerData(pPlayer, HR.PlayerData.index('FAITH')).split("/")
		newFaithData = FaithData[0] + "/" + str(iThreshold)
		HR.setPlayerData(pPlayer, HR.PlayerData.index('FAITH'), newFaithData)



	def increaseFaithThreshold(self, pPlayer):
		''
		iThreshold = self.getFaithThreshold(pPlayer) + self.iThresholdIncrease
		self.setFaith(pPlayer, 0)
		self.setFaithThreshold(pPlayer, iThreshold)

		pCity = HR.getRandomCity(pPlayer)
		if pCity != None:
			if pPlayer.isCivic(Tenets().AnyGreatPersonFaith):
				GPList = []
				GPList += HR.GreatPeople
				GPList.append(gc.getInfoTypeForString('UNIT_PROPHET'))
				GPList.append(gc.getInfoTypeForString('UNIT_GENERAL'))
				iUnit = GPList[CyGame().getSorenRandNum(len(GPList), "Random Great Person from Faith")]
			else:
				iUnit = gc.getInfoTypeForString('UNIT_PROPHET')

			try:
				pCity.createGreatPeople(iUnit, False, False)

			except:
				# Workaround for 'unidentifiable C++ exception' and 'Memory Error'
				UnitInfo = gc.getUnitInfo(iUnit)
				iCount = pPlayer.getUnitClassCount(UnitInfo.getUnitClassType())

				print "FAITH: Error in increaseFaithThreshold (" + pCity.getName() + ", Unit ID: " + str(iUnit) + ", Count: " + str(iCount) + ")"

				if iCount == 0:
					iAIType = UnitInfo.getDefaultUnitAIType()
					pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes(iAIType), DirectionTypes.NO_DIRECTION)

					for iRival in xrange(gc.getMAX_CIV_PLAYERS()):
						pRival = gc.getPlayer(iRival)
						if pCity.isRevealed(pRival.getTeam(), False):
							CyInterface().addMessage(iRival, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText('TXT_KEY_MISC_GP_BORN', (UnitInfo.getDescription(), pCity.getName())), 'AS2D_UNIT_GREATPEOPLE', InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, UnitInfo.getButton(), gc.getInfoTypeForString('COLOR_UNIT_TEXT'), pCity.getX(), pCity.getY(), True, True)

						else:
							CyInterface().addMessage(iRival, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText('TXT_KEY_MISC_GP_BORN_SOMEWHERE', (UnitInfo.getDescription(), )), 'AS2D_UNIT_GREATPEOPLE', InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, '', gc.getInfoTypeForString('COLOR_UNIT_TEXT'), -1, -1, False, False)

		return iThreshold



	def getFaithTotal(self, pPlayer):
		''
		FaithData = HR.getPlayerData(pPlayer, HR.PlayerData.index('FAITH')).split("/")
		iFaith = int(FaithData[0])
		iThreshold = int(FaithData[1])

		iFaithTotal = iFaith
		for i in xrange(iThreshold / self.iThresholdIncrease):
			iFaithTotal += (i * self.iThresholdIncrease)

		return iFaithTotal



	def getFaithTurns(self, pPlayer):
		''
		iThreshold = self.getFaithThreshold(pPlayer)
		iProgress = self.getFaith(pPlayer)
		iRate = self.getFaithRate(pPlayer)
		if iRate > 0:
			iTurns = (iThreshold - iProgress + iRate - 1) / iRate
			return iTurns

		return -1



	def getFaithInfluence(self, pPlayer, pRival):
		''
		iReligion = pPlayer.getStateReligion()
		if iReligion == -1 or pRival.getStateReligion() != iReligion:
			return 0

		iPlayerFaith = Faith().getFaithTotal(pPlayer)
		iRivalFaith = Faith().getFaithTotal(pRival)
		iChance = 25 + ((iPlayerFaith - iRivalFaith) * 5 / self.iThresholdIncrease)

		iInfluenceTenet, iInfluenceModifier = Tenets().ReformationInfluenceModifier
		if pPlayer.isCivic(iInfluenceTenet):
			iChance += 25

		iChance = min(99, iChance)
		iChance = max(-99, iChance)

		return iChance



	def getHighestFaithPlayer(self, iReligion, iIgnorePlayer):
		'Returns the ID of the player with this religion that has the highest faith'
		'Can ignore a particular player - e.g. the player that just converted'
		iFaithLeader = -1
		iHighestFaith = -1

		for iPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
			if iPlayer == iIgnorePlayer:
				continue

			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isAlive() and pPlayer.getStateReligion() == iReligion:
				iFaith = self.getFaithTotal(pPlayer)
				if iFaith > iHighestFaith:
					iHighestFaith = iFaith
					iFaithLeader = iPlayer

		return iFaithLeader



	def getFaithBarHelp(self, pPlayer):
		'Provides help text for the Faith bar'
		szUnit = gc.getUnitInfo(gc.getInfoTypeForString('UNIT_PROPHET')).getDescription()
		iFaith = self.getFaith(pPlayer)
		iFaithThreshold = self.getFaithThreshold(pPlayer)
		iTurns = self.getFaithTurns(pPlayer)
		iReligion = pPlayer.getStateReligion()

		szBullet = u"%c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)
		szHelp = CyTranslator().getText('TXT_KEY_INTERFACE_FAITH_BAR_HELP', (iFaith, iFaithThreshold))
		szHelp += "\n" + CyTranslator().getText('TXT_KEY_INTERFACE_FAITH_BAR_HELP_2', (szUnit, iTurns))

		iBuildingFaith = 0
		iWonderFaith = 0
		iNonStateFaith = 0
		iSpecialistFaith = 0

		(loopCity, iter) = pPlayer.firstCity(False)
		while(loopCity):
			iBuildingFaith += self.getFaithFromBuildings(loopCity, True, False, False)
			iWonderFaith += self.getFaithFromBuildings(loopCity, False, True, False)
			iNonStateFaith += self.getFaithFromBuildings(loopCity, False, False, True)
			iSpecialistFaith += self.getFaithFromSpecialists(loopCity)
			(loopCity, iter) = pPlayer.nextCity(iter, False)

		iForeignFaith = self.getFaithFromForeignBuildings(pPlayer)
		iResourceFaith = self.getFaithFromResources(pPlayer)

		iTotalFaith = iBuildingFaith + iNonStateFaith + iForeignFaith + iWonderFaith + iSpecialistFaith + iResourceFaith
		iFaithModifier = self.getFaithModifier(pPlayer)
		iModifiedFaith = (iTotalFaith * iFaithModifier / 100)
		iTotalFaith += iModifiedFaith

		if iBuildingFaith > 0:
			szHelp += u"\n%s+%d%c from Buildings" % (szBullet, iBuildingFaith, CyGame().getSymbolID(FontSymbols.RELIGION_CHAR))
		if iNonStateFaith > 0:
			szHelp += u"\n%s+%d%c from Buildings (Non-State)" % (szBullet, iNonStateFaith, CyGame().getSymbolID(FontSymbols.RELIGION_CHAR))
		if iForeignFaith > 0:
			szHelp += u"\n%s+%d%c from Buildings (Foreign)" % (szBullet, iForeignFaith, CyGame().getSymbolID(FontSymbols.RELIGION_CHAR))
		if iWonderFaith > 0:
			szHelp += u"\n%s+%d%c from Wonders" % (szBullet, iWonderFaith, CyGame().getSymbolID(FontSymbols.RELIGION_CHAR))
		if iSpecialistFaith > 0:
			szHelp += u"\n%s+%d%c from Specialists" % (szBullet, iSpecialistFaith, CyGame().getSymbolID(FontSymbols.RELIGION_CHAR))
		if iResourceFaith > 0:
			szHelp += u"\n%s+%d%c from Resources" % (szBullet, iResourceFaith, CyGame().getSymbolID(FontSymbols.RELIGION_CHAR))
		if iModifiedFaith > 0:
			szHelp += u"\n%s+%d%c from Modifier (%d%%)" % (szBullet, iModifiedFaith, CyGame().getSymbolID(FontSymbols.RELIGION_CHAR), iFaithModifier)

		if iTotalFaith > 0:
			szTotal = u"\n%s+%d%c per Turn" % (szBullet, iTotalFaith, CyGame().getSymbolID(FontSymbols.RELIGION_CHAR))
			szHelp += CyTranslator().changeTextColor(szTotal, gc.getInfoTypeForString('COLOR_SELECTED_TEXT'))

		if iReligion > -1:
			lInfluenceOn = []
			lInfluenceBy = []
			for iRival in xrange(gc.getMAX_CIV_PLAYERS()):
				pRival = gc.getPlayer(iRival)
				if not pRival.isAlive() or iRival == pPlayer.getID():
					continue
				if not gc.getTeam(pPlayer.getTeam()).isHasMet(pRival.getTeam()):
					continue
				if pRival.getStateReligion() == iReligion:
					if not pRival.isCivic(Tenets().ForeignReformationImmunity):
						iOnChance = self.getFaithInfluence(pPlayer, pRival)
						if iOnChance > 0:
							lInfluenceOn.append((iOnChance, pRival))

					if not pPlayer.isCivic(Tenets().ForeignReformationImmunity):
						iByChance = self.getFaithInfluence(pRival, pPlayer)
						if iByChance > 0:
							lInfluenceBy.append((iByChance, pRival))

			if lInfluenceOn:
				lInfluenceOn.sort()
				lInfluenceOn.reverse()
				szHelp += "\n\n" + CyTranslator().getText('TXT_KEY_INTERFACE_FAITH_BAR_HELP_3', ())
				for iChance, pRival in lInfluenceOn:
					szColor = u"<color=%d,%d,%d,%d>" % (pRival.getPlayerTextColorR(), pRival.getPlayerTextColorG(), pRival.getPlayerTextColorB(), pRival.getPlayerTextColorA())
					szHelp += "\n" + str(iChance) + "%\t" + szColor + pRival.getCivilizationDescription(0) + "</color>"

			if lInfluenceBy:
				lInfluenceBy.sort()
				lInfluenceBy.reverse()
				szHelp += "\n\n" + CyTranslator().getText('TXT_KEY_INTERFACE_FAITH_BAR_HELP_4', ())
				for iChance, pRival in lInfluenceBy:
					szColor = u"<color=%d,%d,%d,%d>" % (pRival.getPlayerTextColorR(), pRival.getPlayerTextColorG(), pRival.getPlayerTextColorB(), pRival.getPlayerTextColorA())
					szHelp += "\n" + str(iChance) + "%\t" + szColor + pRival.getCivilizationDescription(0) + "</color>"

		return szHelp



	def getCityFaithBarHelp(self, pCity):
		''
		pPlayer = gc.getPlayer(pCity.getOwner())

		szUnit = gc.getUnitInfo(gc.getInfoTypeForString('UNIT_PROPHET')).getDescription()
		szBullet = u"%c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)
		szHelp = CyTranslator().changeTextColor(szUnit, gc.getInfoTypeForString('COLOR_GREAT_PEOPLE_RATE'))

		iBuildingFaith = self.getFaithFromBuildings(pCity, True, False, False)
		iNonStateFaith = self.getFaithFromBuildings(pCity, False, False, True)
		iWonderFaith = self.getFaithFromBuildings(pCity, False, True, False)
		iSpecialistFaith = self.getFaithFromSpecialists(pCity)

		iTotalFaith = iBuildingFaith + iNonStateFaith + iWonderFaith + iSpecialistFaith
		iFaithModifier = self.getFaithModifier(pPlayer)
		iModifiedFaith = (iTotalFaith * iFaithModifier / 100)

		if iBuildingFaith > 0:
			szHelp += u"\n%s+%d%c from Buildings" % (szBullet, iBuildingFaith, CyGame().getSymbolID(FontSymbols.RELIGION_CHAR))
		if iNonStateFaith > 0:
			szHelp += u"\n%s+%d%c from Buildings (Non-State)" % (szBullet, iNonStateFaith, CyGame().getSymbolID(FontSymbols.RELIGION_CHAR))
		if iWonderFaith > 0:
			szHelp += u"\n%s+%d%c from Wonders" % (szBullet, iWonderFaith, CyGame().getSymbolID(FontSymbols.RELIGION_CHAR))
		if iSpecialistFaith > 0:
			szHelp += u"\n%s+%d%c from Specialists" % (szBullet, iSpecialistFaith, CyGame().getSymbolID(FontSymbols.RELIGION_CHAR))
		if iModifiedFaith > 0:
			szHelp += u"\n%s+%d%c from Modifier (%d%)" % (szBullet, iModifiedFaith, CyGame().getSymbolID(FontSymbols.RELIGION_CHAR), iFaithModifier)

		return szHelp



class Tenets:
	def __init__(self):

		self.AllowInquisitors				 = gc.getInfoTypeForString('CIVIC_TENET_PERSECUTION')
		self.AllowRepentance				 = gc.getInfoTypeForString('CIVIC_TENET_APOSTASY')
		self.AnyGreatPersonFaith			 = gc.getInfoTypeForString('CIVIC_TENET_HUMANISM')
		self.ApostasyAttitudeChange		 	 = gc.getInfoTypeForString('CIVIC_TENET_APOSTASY'), -2
		self.ChangeGreatTempleRequirement	 = gc.getInfoTypeForString('CIVIC_TENET_PANTHEISM'), -2
		self.ChangeMonasteryRequirement		 = gc.getInfoTypeForString('CIVIC_TENET_ETHICISM'), -1
		self.DissentModifier				 = gc.getInfoTypeForString('CIVIC_TENET_JUDGEMENT'), -25
		self.FoodStoredModifier				 = gc.getInfoTypeForString('CIVIC_TENET_SACRIFICE'), -100
		self.ForeignBuildingFaith			 = gc.getInfoTypeForString('CIVIC_TENET_MONOTHEISM'), 50
		self.ForeignReformationImmunity		 = gc.getInfoTypeForString('CIVIC_TENET_INSULARITY')
		self.GoldenAgeFaithModifier			 = gc.getInfoTypeForString('CIVIC_TENET_ETHICISM'), 100
		self.GoldenAgeLengthModifier		 = gc.getInfoTypeForString('CIVIC_TENET_IDOLATRY'), -50
		self.GreatSpecialistFaith			 = gc.getInfoTypeForString('CIVIC_TENET_ENLIGHTENMENT'), 5
		self.HeathenCombatFaith				 = gc.getInfoTypeForString('CIVIC_TENET_SALVATION'), 1
		self.MilitaryUnitCostModifier		 = gc.getInfoTypeForString('CIVIC_TENET_MEDITATION'), 25
		self.MissionarySuccess				 = gc.getInfoTypeForString('CIVIC_TENET_PROSELYTISM')
		self.MonasteryExperience			 = gc.getInfoTypeForString('CIVIC_TENET_DISCIPLINE'), 2
		self.MonasteryTradeRoutes			 = gc.getInfoTypeForString('CIVIC_TENET_PILGRIMAGE'), 1
		self.NoDefyResolutionAnger			 = gc.getInfoTypeForString('CIVIC_TENET_INSULARITY')
		self.NoNonStateReligionDissent		 = gc.getInfoTypeForString('CIVIC_TENET_PLURALISM')
		self.NoReformationAnarchy			 = gc.getInfoTypeForString('CIVIC_TENET_SYNCRETISM')
		self.NoStateReligion				 = gc.getInfoTypeForString('CIVIC_TENET_APOSTASY')
		self.NonStateBuildingFaith			 = gc.getInfoTypeForString('CIVIC_TENET_PANTHEISM'), 50
		self.ReligiousSimilarityModifier	 = gc.getInfoTypeForString('CIVIC_TENET_SYNCRETISM'), 50
		self.ReligiousDifferenceModifier	 = gc.getInfoTypeForString('CIVIC_TENET_FORBEARANCE'), -50
		self.ReformationInfluenceModifier	 = gc.getInfoTypeForString('CIVIC_TENET_FORBEARANCE'), 25
		self.ShrineGPPModifier				 = gc.getInfoTypeForString('CIVIC_TENET_PILGRIMAGE'), 50
		self.StateReligionGPPModifier		 = gc.getInfoTypeForString('CIVIC_TENET_MONOTHEISM'), 25, -10
		self.StateReligionSpreadTemple		 = gc.getInfoTypeForString('CIVIC_TENET_PROSELYTISM')
		self.TempleGPPModifier				 = gc.getInfoTypeForString('CIVIC_TENET_ENLIGHTENMENT'), 25
		self.TempleHappiness				 = gc.getInfoTypeForString('CIVIC_TENET_SALVATION'), 1
		self.TempleHealth					 = gc.getInfoTypeForString('CIVIC_TENET_PRESERVATION'), 1
		self.WonderCostModifier				 = gc.getInfoTypeForString('CIVIC_TENET_IDOLATRY'), 25
		self.WonderFaith					 = gc.getInfoTypeForString('CIVIC_TENET_PRESERVATION'), 2
		self.WonderPopulationChange			 = gc.getInfoTypeForString('CIVIC_TENET_SACRIFICE'), -1

		self.AdvisorBuildingCostModifier	 =[(gc.getInfoTypeForString('CIVIC_TENET_POLYTHEISM'),		-25, gc.getInfoTypeForString('ADVISOR_RELIGION')),
											   (gc.getInfoTypeForString('CIVIC_TENET_HUMANISM'),		-25, gc.getInfoTypeForString('ADVISOR_SCIENCE')),
										 	   (gc.getInfoTypeForString('CIVIC_TENET_HEDONISM'),		-25, gc.getInfoTypeForString('ADVISOR_CULTURE')),
										 	   (gc.getInfoTypeForString('CIVIC_TENET_DUTY'),			-25, gc.getInfoTypeForString('ADVISOR_MILITARY')),
											   (gc.getInfoTypeForString('CIVIC_TENET_ALTRUISM'),		-25, gc.getInfoTypeForString('ADVISOR_GROWTH'))]

		self.FaithResources					 = {gc.getInfoTypeForString('BONUSCLASS_ANIMALS'): 			(gc.getInfoTypeForString('CIVIC_TENET_ANIMISM'), 1),
												gc.getInfoTypeForString('BONUSCLASS_CROPS'): 			(gc.getInfoTypeForString('CIVIC_TENET_FERTILITY'), 1),
												gc.getInfoTypeForString('BONUSCLASS_LUXURIES'):			(gc.getInfoTypeForString('CIVIC_TENET_PROSPERITY'), 1),
												gc.getInfoTypeForString('BONUSCLASS_MATERIALS'):		(gc.getInfoTypeForString('CIVIC_TENET_ORDER'), 1)}

		self.GreatPersonTypeModifier 		 = {gc.getInfoTypeForString('UNIT_DOCTOR'): 				(gc.getInfoTypeForString('CIVIC_TENET_PRAYER'), -50),
												gc.getInfoTypeForString('UNIT_SCIENTIST'):				(gc.getInfoTypeForString('CIVIC_TENET_PRAYER'), -50)}

		self.TempleYield					 = {gc.getInfoTypeForString('CIVIC_TENET_FERTILITY'):		(YieldTypes.YIELD_FOOD, 1),
												gc.getInfoTypeForString('CIVIC_TENET_ORDER'):			(YieldTypes.YIELD_PRODUCTION, 1),
												gc.getInfoTypeForString('CIVIC_TENET_PROSPERITY'):		(YieldTypes.YIELD_COMMERCE, 1)}

		self.MonasteryCommerce				 = {gc.getInfoTypeForString('CIVIC_TENET_SUPERSTITION'):	(CommerceTypes.COMMERCE_CULTURE, 2),
												gc.getInfoTypeForString('CIVIC_TENET_OCCULTISM'):		(CommerceTypes.COMMERCE_ESPIONAGE, 2),
												gc.getInfoTypeForString('CIVIC_TENET_SCRIPTURE'):		(CommerceTypes.COMMERCE_GOLD, 2),
												gc.getInfoTypeForString('CIVIC_TENET_RATIONALISM'):		(CommerceTypes.COMMERCE_RESEARCH, 2)}

		self.GreatTemplePromotion			 = {gc.getInfoTypeForString('CIVIC_TENET_HEDONISM'):		(gc.getInfoTypeForString('PROMOTION_CITY_RAIDER1'), []),
												gc.getInfoTypeForString('CIVIC_TENET_HONOUR'):			(gc.getInfoTypeForString('PROMOTION_LEADERSHIP'), []),
												gc.getInfoTypeForString('CIVIC_TENET_PURITY'):			(gc.getInfoTypeForString('PROMOTION_MARCH'), [])}

		self.GreatTempleSpecialist			 = {gc.getInfoTypeForString('CIVIC_TENET_ALTRUISM'):		(gc.getInfoTypeForString('SPECIALIST_DOCTOR')),
												gc.getInfoTypeForString('CIVIC_TENET_DUTY'):			(gc.getInfoTypeForString('SPECIALIST_ENGINEER')),
												gc.getInfoTypeForString('CIVIC_TENET_JUDGEMENT'):		(gc.getInfoTypeForString('SPECIALIST_SPY')),
												gc.getInfoTypeForString('CIVIC_TENET_OCCULTISM'):		(gc.getInfoTypeForString('SPECIALIST_MERCHANT')),
												gc.getInfoTypeForString('CIVIC_TENET_SCRIPTURE'):		(gc.getInfoTypeForString('SPECIALIST_PRIEST')),
												gc.getInfoTypeForString('CIVIC_TENET_DISCIPLINE'):		(gc.getInfoTypeForString('SPECIALIST_ARTIST')),
												gc.getInfoTypeForString('CIVIC_TENET_RATIONALISM'):		(gc.getInfoTypeForString('SPECIALIST_SCIENTIST'))}

		self.NaturalWonderSpecialists		 = {gc.getInfoTypeForString('CIVIC_TENET_ANIMISM'):			gc.getInfoTypeForString('SPECIALIST_PRIEST')}

		self.FixedTenets					 = {gc.getInfoTypeForString('RELIGION_PESEDJET'):			gc.getInfoTypeForString('CIVIC_TENET_POLYTHEISM'),
												gc.getInfoTypeForString('RELIGION_ANUNNAKI'):			gc.getInfoTypeForString('CIVIC_TENET_POLYTHEISM'),
												gc.getInfoTypeForString('RELIGION_BAALISM'):			gc.getInfoTypeForString('CIVIC_TENET_POLYTHEISM'),
												gc.getInfoTypeForString('RELIGION_JUDAISM'):			gc.getInfoTypeForString('CIVIC_TENET_MONOTHEISM'),
												gc.getInfoTypeForString('RELIGION_CHRISTIANITY'):		gc.getInfoTypeForString('CIVIC_TENET_MONOTHEISM'),
												gc.getInfoTypeForString('RELIGION_ISLAM'):				gc.getInfoTypeForString('CIVIC_TENET_MONOTHEISM'),
												gc.getInfoTypeForString('RELIGION_ZOROASTRIANISM'):		gc.getInfoTypeForString('CIVIC_TENET_PANTHEISM'),
												gc.getInfoTypeForString('RELIGION_HINDUISM'):			gc.getInfoTypeForString('CIVIC_TENET_PANTHEISM'),
												gc.getInfoTypeForString('RELIGION_BUDDHISM'):			gc.getInfoTypeForString('CIVIC_TENET_ETHICISM'),
												gc.getInfoTypeForString('RELIGION_CONFUCIANISM'):		gc.getInfoTypeForString('CIVIC_TENET_ETHICISM'),
												gc.getInfoTypeForString('RELIGION_TAOISM'):				gc.getInfoTypeForString('CIVIC_TENET_ETHICISM'),
												gc.getInfoTypeForString('RELIGION_SHINTO'):				gc.getInfoTypeForString('CIVIC_TENET_ANIMISM'),
												gc.getInfoTypeForString('RELIGION_OLYMPIANISM'):		gc.getInfoTypeForString('CIVIC_TENET_POLYTHEISM'),
												gc.getInfoTypeForString('RELIGION_DRUIDISM'):			gc.getInfoTypeForString('CIVIC_TENET_ANIMISM'),
												gc.getInfoTypeForString('RELIGION_ASATRU'):				gc.getInfoTypeForString('CIVIC_TENET_POLYTHEISM'),
												gc.getInfoTypeForString('RELIGION_SHAMANISM'):			gc.getInfoTypeForString('CIVIC_TENET_ANIMISM'),
												gc.getInfoTypeForString('RELIGION_TEOTL'):				gc.getInfoTypeForString('CIVIC_TENET_PANTHEISM'),
												gc.getInfoTypeForString('RELIGION_VODUN'):				gc.getInfoTypeForString('CIVIC_TENET_ANIMISM')}

		self.IdealTenets					 = {gc.getInfoTypeForString('RELIGION_PESEDJET'):			gc.getInfoTypeForString('CIVIC_TENET_PRESERVATION'),
												gc.getInfoTypeForString('RELIGION_ANUNNAKI'):			gc.getInfoTypeForString('CIVIC_TENET_ORDER'),
												gc.getInfoTypeForString('RELIGION_BAALISM'):			gc.getInfoTypeForString('CIVIC_TENET_PROSPERITY'),
												gc.getInfoTypeForString('RELIGION_JUDAISM'):			gc.getInfoTypeForString('CIVIC_TENET_SCRIPTURE'),
												gc.getInfoTypeForString('RELIGION_CHRISTIANITY'):		gc.getInfoTypeForString('CIVIC_TENET_SALVATION'),
												gc.getInfoTypeForString('RELIGION_ISLAM'):				gc.getInfoTypeForString('CIVIC_TENET_PILGRIMAGE'),
												gc.getInfoTypeForString('RELIGION_ZOROASTRIANISM'):		gc.getInfoTypeForString('CIVIC_TENET_PURITY'),
												gc.getInfoTypeForString('RELIGION_HINDUISM'):			gc.getInfoTypeForString('CIVIC_TENET_MEDITATION'),
												gc.getInfoTypeForString('RELIGION_BUDDHISM'):			gc.getInfoTypeForString('CIVIC_TENET_ENLIGHTENMENT'),
												gc.getInfoTypeForString('RELIGION_TAOISM'):				gc.getInfoTypeForString('CIVIC_TENET_DISCIPLINE'),
												gc.getInfoTypeForString('RELIGION_CONFUCIANISM'):		gc.getInfoTypeForString('CIVIC_TENET_DUTY'),
												gc.getInfoTypeForString('RELIGION_SHINTO'):				gc.getInfoTypeForString('CIVIC_TENET_HONOUR'),
												gc.getInfoTypeForString('RELIGION_OLYMPIANISM'):		gc.getInfoTypeForString('CIVIC_TENET_JUDGEMENT'),
												gc.getInfoTypeForString('RELIGION_DRUIDISM'):			gc.getInfoTypeForString('CIVIC_TENET_CEREMONY'),
												gc.getInfoTypeForString('RELIGION_ASATRU'):				gc.getInfoTypeForString('CIVIC_TENET_HEDONISM'),
												gc.getInfoTypeForString('RELIGION_SHAMANISM'):			gc.getInfoTypeForString('CIVIC_TENET_IDOLATRY'),
												gc.getInfoTypeForString('RELIGION_TEOTL'):				gc.getInfoTypeForString('CIVIC_TENET_SACRIFICE'),
												gc.getInfoTypeForString('RELIGION_VODUN'):				gc.getInfoTypeForString('CIVIC_TENET_OCCULTISM')}

		self.TenetTechs						 = {gc.getInfoTypeForString('CIVIC_TENET_HUMANISM'):		gc.getInfoTypeForString('TECH_ACADEMIA'),
												gc.getInfoTypeForString('CIVIC_TENET_PRESERVATION'):	gc.getInfoTypeForString('TECH_PRIESTHOOD'),
												gc.getInfoTypeForString('CIVIC_TENET_SALVATION'):		gc.getInfoTypeForString('TECH_THEOLOGY'),
												gc.getInfoTypeForString('CIVIC_TENET_ENLIGHTENMENT'):	gc.getInfoTypeForString('TECH_HUMANITIES'),
												gc.getInfoTypeForString('CIVIC_TENET_PURITY'):			gc.getInfoTypeForString('TECH_MEDICINE'),
												gc.getInfoTypeForString('CIVIC_TENET_ALTRUISM'):		gc.getInfoTypeForString('TECH_ETHICS'),
												gc.getInfoTypeForString('CIVIC_TENET_HONOUR'):			gc.getInfoTypeForString('TECH_WARRIOR_CODE'),
												gc.getInfoTypeForString('CIVIC_TENET_DUTY'):			gc.getInfoTypeForString('TECH_PATRONAGE'),
												gc.getInfoTypeForString('CIVIC_TENET_JUDGEMENT'):		gc.getInfoTypeForString('TECH_JUDICIARY'),
												gc.getInfoTypeForString('CIVIC_TENET_OCCULTISM'):		gc.getInfoTypeForString('TECH_ASTROLOGY'),
												gc.getInfoTypeForString('CIVIC_TENET_SCRIPTURE'):		gc.getInfoTypeForString('TECH_WRITING'),
												gc.getInfoTypeForString('CIVIC_TENET_PILGRIMAGE'):		gc.getInfoTypeForString('TECH_COMPASS'),
												gc.getInfoTypeForString('CIVIC_TENET_DISCIPLINE'):		gc.getInfoTypeForString('TECH_AESTHETICS'),
												gc.getInfoTypeForString('CIVIC_TENET_RATIONALISM'):		gc.getInfoTypeForString('TECH_EDUCATION'),
												gc.getInfoTypeForString('CIVIC_TENET_APOSTASY'):		gc.getInfoTypeForString('TECH_SCIENTIFIC_METHOD')}



	def isTenet(self, iCivic):
		'Returns true if the specified civic is actually a tenet'
		if gc.getCivicInfo(iCivic).getType().find("_TENET_") > 0:
			return True

		return False



	def isTenetCategory(self, iCategory):
		'Returns true if the specified category is actually a tenet category'
		if gc.getCivicOptionInfo(iCategory).getType().find("_TENET_") > 0:
			return True

		return False



	def getTenetData(self, pPlayer):
		''
		TenetList = []
		TenetData = HR.getPlayerData(pPlayer, HR.PlayerData.index('TENETS')).split(",")
		for szData in TenetData:
			TenetList.append(int(szData))

		return TenetList



	def setTenetData(self, pPlayer, TenetList):
		''
		TenetData = ""
		for iTenet in TenetList:
			TenetData += str(iTenet)
			TenetData += ","
		TenetData = TenetData[:-1]

		HR.setPlayerData(pPlayer, HR.PlayerData.index('TENETS'), TenetData)



	def couldReformTenet(self, pPlayer, iTenet):
		'Returns true if the player could choose this tenet during a reformation'

		# Tech needed
		if iTenet in self.TenetTechs.keys():
			iTech = self.TenetTechs[iTenet]
			if iTech > -1:
				if gc.getTeam(pPlayer.getTeam()).isHasTech(iTech):
					return True
				else:
					return False

		# Fixed Tenets
		iReligion = pPlayer.getStateReligion()
		if iReligion in self.FixedTenets:
			iFixedTenet = self.FixedTenets[iReligion]
			if iTenet != iFixedTenet:
				iCategory = gc.getCivicInfo(iTenet).getCivicOptionType()
				iFixedCategory = gc.getCivicInfo(iFixedTenet).getCivicOptionType()
				if iCategory == iFixedCategory:
					iBuilding = HR.getPlayerBuilding(pPlayer, HR.Building.AllowFixedTenets)
					if pPlayer.countNumBuildings(iBuilding) == 0:
						return False

		return True



	def onTenetChanged(self, pPlayer, iTenet, bAdopted):
		'Event triggered when a specified tenet has been changed for a player'
		iStateReligion = pPlayer.getStateReligion()
		iYieldType = -1
		iYieldChange = 0
		iHappyChange = 0
		iHealthChange = 0
		iTradeRoutes = 0
		iSpecialist = -1
		iTemple = -1
		iGreatTemple = -1
		iMonastery = -1

		# Religious Building Effects
		if iStateReligion > -1:
			iTemple = getReligionTemple(iStateReligion)
			iGreatTemple = getReligionGreatTemple(iStateReligion)
			iMonastery = getReligionMonastery(iStateReligion)

			# Temples
			if iTenet in self.TempleYield.keys():
				iYieldType, iYieldChange = self.TempleYield[iTenet]
				if not bAdopted:
					iYieldChange = 0

			if iTenet == self.TempleHappiness[0]:
				iHappyChange = self.TempleHappiness[1]
				if not bAdopted:
					iHappyChange *= -1

			if iTenet == self.TempleHealth[0]:
				iHealthChange = self.TempleHappiness[1]
				if not bAdopted:
					iHealthChange *= -1

			# Great Temples
			if iTenet in self.GreatTempleSpecialist.keys():
				iSpecialist = self.GreatTempleSpecialist[iTenet]

			# Monasteries
			if iTenet == self.MonasteryTradeRoutes[0]:
				iTradeRoutes = self.MonasteryTradeRoutes[1]
				if not bAdopted:
					iTradeRoutes *= -1

		# City Effects
		(loopCity, iter) = pPlayer.firstCity(False)
		while(loopCity):

			# Temples
			if iTemple > -1:
				if iYieldType > -1:
					iTempleClass = gc.getBuildingInfo(iTemple).getBuildingClassType()
					loopCity.setBuildingYieldChange(iTempleClass, iYieldType, iYieldChange)

				if loopCity.getNumBuilding(iTemple) > 0:
					if iHappyChange != 0:
						loopCity.changeExtraHappiness(iHappyChange)
					if iHealthChange != 0:
						loopCity.changeExtraHealth(iHealthChange)

			# Great Temples
			if iGreatTemple > -1:
				if loopCity.getNumBuilding(iGreatTemple) > 0:
					if iSpecialist > -1:
						if bAdopted:
							loopCity.changeFreeSpecialistCount(iSpecialist, 1)
						else:
							loopCity.changeFreeSpecialistCount(iSpecialist, -1)

			# Monasteries
			if iMonastery > -1 and iTradeRoutes != 0:
				if loopCity.getNumBuilding(iMonastery) > 0:
					loopCity.changeExtraTradeRoutes(iTradeRoutes)

			# Natural Wonder Specialists
			for iNWTenet, iNWSpecialist in self.NaturalWonderSpecialists.items():
				if iTenet == iNWTenet:
					for iNW in HR_Map.NaturalWonders().NaturalWonders.keys():
						sType = gc.getFeatureInfo(iNW).getType().replace("FEATURE_", "BUILDING_")
						iNWBuilding = gc.getInfoTypeForString(sType)
						if loopCity.getNumBuilding(iNWBuilding) > 0:
							if bAdopted:
								loopCity.changeFreeSpecialistCount(iNWSpecialist, 1)
							else:
								loopCity.changeFreeSpecialistCount(iNWSpecialist, -1)

			(loopCity, iter) = pPlayer.nextCity(iter, False)

		# Inquisitors
		if iTenet == self.AllowInquisitors and not bAdopted:
			(loopUnit, iter) = pPlayer.firstUnit(False)
			while(loopUnit):
				if loopUnit.getUnitType() == Inquisition().InquisitorUnit:
					loopUnit.kill(False, -1)
				(loopUnit, iter) = pPlayer.nextUnit(iter, False)



	def getReformationTimer(self, pPlayer):
		''
		return int(HR.getPlayerData(pPlayer, HR.PlayerData.index('REFORMATION_TIMER')))



	def setReformationTimer(self, pPlayer, iTurns):
		''
		HR.setPlayerData(pPlayer, HR.PlayerData.index('REFORMATION_TIMER'), str(iTurns))



	def canReformation(self, pPlayer):
		'Returns true if a player is able to reform their tenets'
		if not pPlayer.isAnarchy():
			if pPlayer.getStateReligion() > -1:
				if pPlayer.getRevolutionTimer() == 0:
					if self.getReformationTimer(pPlayer) == 0:
						return True

		return False



	def callReformation(self, pPlayer, TenetList):
		''
		# Human Player
		if pPlayer.isHuman():
			self.setReformationTimer(pPlayer, -1)
			if pPlayer.getID() == CyGame().getActivePlayer() and not CyGame().GetWorldBuilderMode():
				CvScreensInterface.showTenetsScreen()

		# AI Player
		else:
			iReligion = pPlayer.getStateReligion()
			if TenetList == []:
				TenetList = self.selectAITenets(pPlayer, iReligion)

			if pPlayer.getBuildingClassCount(HR.Building.AllowFixedTenets) > 0:
				iFavReligion = gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteReligion()
				if iFavReligion in self.FixedTenets:
					iFavTenet = self.FixedTenets[iFavReligion]
					if not iFavTenet in TenetList:
						iCategory = gc.getCivicInfo(iFavTenet).getCivicOptionType()
						TenetList[iCategory] = iFavTenet

			bAnarchy = True
			if pPlayer.isCivic(self.NoReformationAnarchy) or CivilWar.CivilWar().getAnarchyImmunity(pPlayer) > 0:
				bAnarchy = False

			self.doReformation(pPlayer, TenetList, bAnarchy)



	def doReformation(self, pPlayer, TenetList, bAnarchy):
		''
		iAnarchy = pPlayer.getCivicAnarchyLength(TenetList)
		if bAnarchy:
			pPlayer.changeAnarchyTurns(iAnarchy)

		iTimer = max(1, ((100 + pPlayer.getAnarchyModifier()) * gc.getDefineINT('MIN_REVOLUTION_TURNS') / 100) + iAnarchy)
		self.setReformationTimer(pPlayer, iTimer)

		for iCategory in xrange(len(TenetList)):
			iTenet = TenetList[iCategory]
			if iTenet != pPlayer.getCivics(iCategory):
				pPlayer.setCivics(iCategory, iTenet)

		if pPlayer.getStateReligion() > -1:
			self.doForeignReformation(pPlayer, TenetList)



	def doForeignReformation(self, pPlayer, TenetList):
		''
		iReligion = pPlayer.getStateReligion()
		iPlayerFaith = Faith().getFaithTotal(pPlayer)

		for iRival in xrange(gc.getMAX_CIV_PLAYERS()):
			pRival = gc.getPlayer(iRival)
			if not pRival.isAlive() or iRival == pPlayer.getID():
				continue
			if not gc.getTeam(pPlayer.getTeam()).isHasMet(pRival.getTeam()):
				continue
			if pRival.isCivic(self.ForeignReformationImmunity):
				continue

			iChance = Faith().getFaithInfluence(pPlayer, pRival)
			if iChance < 1:
				continue

			bAnnounced = False
			RivalTenetList = []
			for iCategory in xrange(len(TenetList)):
				iTenet = TenetList[iCategory]
				iRivalTenet = pRival.getCivics(iCategory)
				RivalTenetList.append(iRivalTenet)
				if self.isTenet(iTenet) and iTenet != pRival.getCivics(iCategory):
					if not self.couldReformTenet(pRival, iTenet):
						continue

					if CyGame().getSorenRandNum(100, "Adopt Tenet from Foreign Reformation") < iChance:
						if pRival.isHuman() and not bAnnounced:
							sReligion = gc.getReligionInfo(iReligion).getDescription()
							sCivilization = pPlayer.getCivilizationDescription(0)
							CyInterface().addMessage(iRival, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_FOREIGN_REFORMATION", (sReligion, sCivilization)), "", 0, "", gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"), -1, -1, False, False)
							bAnnounced = True

						pRival.setCivics(iCategory, iTenet)
						RivalTenetList[iCategory] = iTenet

			if not pRival.isCivic(self.NoReformationAnarchy) and CivilWar.CivilWar().getAnarchyImmunity(pRival) == 0:
				iAnarchy = pRival.getCivicAnarchyLength(RivalTenetList)
				pRival.changeAnarchyTurns(iAnarchy)



	def canRepentance(self, pPlayer):
		'Returns true if a player can revert from apostasy'
		if not pPlayer.isAnarchy():
			if not pPlayer.isStateReligion():
				if pPlayer.getRevolutionTimer() == 0:
					if Tenets().getReformationTimer(pPlayer) == 0:
						return True

		return False



	def doRepentance(self, pPlayer):
		''
		iLastReligion = abs(int(HR.getPlayerData(pPlayer, HR.PlayerData.index('STATE_RELIGION')))) - 1
		TenetList = Tenets().selectAITenets(pPlayer, iLastReligion)
		iCategory = gc.getCivicInfo(Tenets().AllowRepentance).getCivicOptionType()
		iTenet = TenetList[iCategory]

		if iTenet == Tenets().AllowRepentance:
			iTenet = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationInitialCivics(iCategory)

		pPlayer.setCivics(iCategory, iTenet)



	def selectAITenets(self, pPlayer, iReligion):
		''
		'Weights are cumulative'
		iWeightIdeal  = 2	# Tenet suited to the religion (listed in Tenets().IdealTenets)
		iWeightFavour = 3	# Favourite Tenet (first listed in CIV4LeaderHeadInfos.xml)
		iWeightPrefer = 2	# Other preferred Tenets (others listed in CIV4LeaderHeadInfos.xml)
		iWeightFaith  =	2	# Tenets of the current Faith Leader
		iWeightFlavor = 2	# Tenets matching desired flavors (listed in CIV4CivicInfos.xml)
		iWeightNormal = 1	# Other tenets

		# Leader Flavors
		LeaderFlavors = []
		for iFlavor in xrange(gc.getNumFlavorTypes()):
			if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFlavorValue(iFlavor) > 0:
				LeaderFlavors.append(iFlavor)

		if pPlayer.AI_isFinancialTrouble():
			LeaderFlavors.append(gc.getInfoTypeForString('FLAVOR_GOLD'))

		# Tenet Choices
		iFixed = -1
		TenetOptions = {}
		print "REFORMATION: " + pPlayer.getName()
		for iTenet in xrange(gc.getNumCivicInfos()):
			if self.isTenet(iTenet):
				TenetInfo = gc.getCivicInfo(iTenet)
				iCategory = TenetInfo.getCivicOptionType()
				if not iCategory in TenetOptions.keys():
					TenetOptions[iCategory] = []
					print gc.getCivicOptionInfo(iCategory).getDescription() + " Options:"
				if not self.couldReformTenet(pPlayer, iTenet):
					continue

				# Tenets to Avoid
				if iTenet in self.getHatedTenets(pPlayer.getLeaderType()):
					continue

				# Ideal Tenets
				if iReligion > -1:
					if self.IdealTenets[iReligion] == iTenet:
						for i in xrange(iWeightIdeal):
							TenetOptions[iCategory].append(iTenet)
							print " - " + TenetInfo.getDescription() + " (Ideal)"

				# Favourite Tenets
				LovedTenets = self.getLovedTenets(pPlayer.getLeaderType())
				if iTenet in LovedTenets:
					if LovedTenets[0] == iTenet:
						for i in xrange(iWeightFavour):
							TenetOptions[iCategory].append(iTenet)
							print " - " + TenetInfo.getDescription() + " (Favourite)"
					else:
						for i in xrange(iWeightPrefer):
							TenetOptions[iCategory].append(iTenet)
							print " - " + TenetInfo.getDescription() + " (Preferred)"

				# Faith Leader
				iFaithLeader = Faith().getHighestFaithPlayer(iReligion, -1)
				if iFaithLeader > -1 and iFaithLeader != pPlayer.getID():
					if iTenet == gc.getPlayer(iFaithLeader).getCivics(iCategory):
						for i in xrange(iWeightFaith):
							TenetOptions[iCategory].append(iTenet)
							print " - " + TenetInfo.getDescription() + " (Faith)"

				# Tenet Flavours
				for iFlavor in self.getTenetFlavors(iTenet):
					if iFlavor in LeaderFlavors:
						for i in xrange(iWeightFlavor):
							TenetOptions[iCategory].append(iTenet)
							print " - " + TenetInfo.getDescription() + " (Flavor)"

				bAvoid = False
				for iFlavor in xrange(gc.getNumFlavorTypes()):
					if iFlavor in self.getTenetBadFlavors(iTenet):
						if iFlavor in LeaderFlavors:
							bAvoid = True
						elif iReligion > -1:
							if gc.getFlavorTypes(iFlavor) == 'FLAVOR_RELIGION':
								if getNumReligionsFounded() < getReligionLimit() or pPlayer.countHolyCities() > 0:
									bAvoid = True

				if not bAvoid:
					for i in xrange(iWeightNormal):
						TenetOptions[iCategory].append(iTenet)
						print " - " + TenetInfo.getDescription() + " (Other)"

		# Determine new Tenets
		ChosenTenets = []
		print "TENETS SELECTED:"
		for iCategory in xrange(gc.getNumCivicOptionInfos()):
			if not iCategory in TenetOptions.keys():
				iSelection = pPlayer.getCivics(iCategory)
				ChosenTenets.append(iSelection)

			elif TenetOptions[iCategory] == []:
				iSelection = pPlayer.getCivics(iCategory)
				ChosenTenets.append(iSelection)
				print " - " + gc.getCivicInfo(iSelection).getDescription() + " (Current)"

			else:
				iSelection = TenetOptions[iCategory][CyGame().getSorenRandNum(len(TenetOptions[iCategory]), "AI Tenet Selection")]
				ChosenTenets.append(iSelection)
				print " - " + gc.getCivicInfo(iSelection).getDescription() + " (Selected)"

		return ChosenTenets



	def getLovedTenets(self, iLeader):
		''
		StringList = str(gc.getLeaderHeadInfo(iLeader).getStrategy()).split()
		TenetList = []

		for string in StringList:
			if string.startswith("TENET_"):
				string = "CIVIC_" + string
				iTenet = gc.getInfoTypeForString(string)
				if iTenet > -1:
					TenetList.append(iTenet)

		return TenetList



	def getHatedTenets(self, iLeader):
		''
		StringList = str(gc.getLeaderHeadInfo(iLeader).getStrategy()).split()
		TenetList = []

		for string in StringList:
			if string.startswith("!TENET_"):
				string = string.replace("!", "")
				string = "CIVIC_" + string
				iTenet = gc.getInfoTypeForString(string)
				if iTenet > -1:
					TenetList.append(iTenet)

		return TenetList



	def getTenetFlavors(self, iTenet):
		''
		StringList = str(gc.getCivicInfo(iTenet).getStrategy()).split()
		FlavorList = []

		for iFlavor in xrange(gc.getNumFlavorTypes()):
			if gc.getFlavorTypes(iFlavor) in StringList:
				FlavorList.append(iFlavor)

		return FlavorList



	def getTenetBadFlavors(self, iTenet):
		''
		StringList = str(gc.getCivicInfo(iTenet).getStrategy()).split()
		FlavorList = []

		for iFlavor in xrange(gc.getNumFlavorTypes()):
			if ("!" + gc.getFlavorTypes(iFlavor)) in StringList:
				FlavorList.append(iFlavor)

		return FlavorList



class Inquisition:
	def __init__(self):
		self.InquisitorUnit = gc.getInfoTypeForString('UNIT_INQUISITOR')



	def doInquisition(self, pUnit, iReligion, pPlayer):
		''
		pCity = pUnit.plot().getPlotCity()
		ReligionInfo = gc.getReligionInfo(iReligion)

		pCity.setHasReligion(iReligion, False, True, True)
		for iPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
			if iPlayer == pPlayer.getID():
				CyInterface().addMessage(iPlayer, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText('TXT_KEY_INQUISITION_SUCCESS', (ReligionInfo.getDescription().capitalize(), pCity.getName(), )), '', 0, ReligionInfo.getButton(), gc.getInfoTypeForString('COLOR_POSITIVE_TEXT'), pCity.getX(), pCity.getY(), True, True)
			elif gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isHasMet(pPlayer.getTeam()):
				CyInterface().addMessage(iPlayer, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText('TXT_KEY_INQUISITION_GLOBAL_MESSAGE', (ReligionInfo.getDescription().capitalize(), pCity.getName(), )), '', 0, ReligionInfo.getButton(), gc.getInfoTypeForString('COLOR_WHITE'), -1, -1, False, False)

		for iBuilding in xrange(gc.getNumBuildingInfos()):
			BuildingInfo = gc.getBuildingInfo(iBuilding)
			if isWorldWonderClass(BuildingInfo.getBuildingClassType()):
				continue
			iReqReligion = BuildingInfo.getPrereqReligion()
			if iReqReligion == iReligion:
				pCity.setNumRealBuilding(iBuilding, 0)

		pUnit.kill(False, -1)



	def doInquisitorAI(self, pUnit, iPlayer):
		''
		pPlayer = gc.getPlayer(iPlayer)
		iStateReligion = pPlayer.getStateReligion()
		pPlot = pUnit.plot()

		lForeign = []
		for iReligion in xrange(gc.getNumReligionInfos()):
			if iStateReligion == iReligion: continue
			if CyGame().isReligionFounded(iReligion):
				lForeign.append(iReligion)

		if pPlot.isCity() and pPlot.getOwner() == iPlayer:
			pCity = pPlot.getPlotCity()
			for iForeign in lForeign:
				if pCity.isHasReligion(iForeign) and not pCity.isHolyCityByType(iForeign):
					self.doInquisition(pUnit, iForeign, pPlayer)
					return

		lCity = []
		(loopCity, iter) = pPlayer.firstCity(False)
		while(loopCity):
			if loopCity.area().getID() == pUnit.area().getID():
				for iForeign in lForeign:
					if loopCity.isHasReligion(iForeign) and not loopCity.isHolyCityByType(iForeign):
						lCity.append(loopCity)
						break
			(loopCity, iter) = pPlayer.nextCity(iter, False)

		if len(lCity) > 0:
			pVictimCity = lCity[CyGame().getSorenRandNum(len(lCity), "Choose City for Inquisition")]
			pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, pVictimCity.getX(), pVictimCity.getY(), 0, False, True, MissionAITypes.NO_MISSIONAI, pPlot, pUnit)



	def shouldTrainInquisitor(self, pCity, iPlayer):
		'Returns true if it is worthwhile for a player to train an Inquisitor'
		pPlayer = gc.getPlayer(iPlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		iStateReligion = pPlayer.getStateReligion()

		if iStateReligion == -1:
			return False
		if pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_INQUISITOR')) > 0:
			return False
		if pTeam.getAtWarCount(True) > 0:
			return False

		lForeign = []
		for iReligion in xrange(gc.getNumReligionInfos()):
			if iStateReligion == iReligion:
				continue
			if CyGame().isReligionFounded(iReligion):
				lForeign.append(iReligion)

		(loopCity, iter) = pPlayer.firstCity(False)
		while(loopCity):
			if loopCity.area().getID() == pCity.area().getID():
				for iForeign in lForeign:
					if loopCity.isHasReligion(iForeign) and not loopCity.isHolyCityByType(iForeign):
						return True
			(loopCity, iter) = pPlayer.nextCity(iter, False)

		return False