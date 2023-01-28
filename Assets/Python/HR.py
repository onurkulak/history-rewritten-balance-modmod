from CvPythonExtensions import *
import BugPath
import CivilWar
import HR_Cities
import HR_Organizations
import HR_Religion

gc = CyGlobalContext()



### Globals

PlayerData =   ['CIVICS',
				'TENETS',
				'STATE_RELIGION',
				'FAITH',
				'REFORMATION_TIMER',
				'ANARCHY_IMMUNITY',
				'SHARES',
				'TRADES']

CityData = 	   ['CITY_ID',
				'GREAT_PEOPLE_PROGRESS',
				'DISSENT',
				'CULTURE_LEVEL',
				'CORPORATE_HAPPINESS',
				'CORPORATE_HEALTH',
				'CORPORATE_YIELD',
				'STARVATION']

Mission = 	   {'MISSION_HUMANITARIAN'			:	910,
				'MISSION_FOUND_RELIGION'		:	940,
				'MISSION_REFORMATION'			:	941,
				'MISSION_REFORMATION_RESOLVE'	:	942,
				'MISSION_REPENTANCE'			:	943,
				'MISSION_GREAT_TEMPLE'			:	944,
				'MISSION_INQUISITION'			:	990}

Interface =	   {'CHANGE_COMMERCE_PERCENT'		:	1200,
				'CHANGE_SPECIALIST'				:	1201,
				'BUY_SHARE'						:	1202,
				'SELL_SHARE'					:	1203,
				'CANCEL_TRADE'					:	1204}



Civic		= 0
Improvement	= 0
Trait		= 0
Unit		= 0

iUnitCaptureChance		= 20
iUnitEnslaveChance		= 20

GreatPeople = []
GreatSpecialist = []
PowerPriority = []

WorldWonderLimits = (0, 0, 1, 2, 4, 6, 8)



### Classes

def init():
	'Initializes expanded options'
	global Civic
	global Trait
	global Unit
	global Building
	global Improvement
	global GreatPeople
	global GreatSpecialist
	global PowerPriority

	Civic = ExpandedCivicOptions()
	Trait = ExpandedTraitOptions()
	Unit = ExpandedUnitOptions()
	Building = ExpandedBuildingOptions()
	Improvement = ExpandedImprovementOptions()

	GreatPeople 	 = [gc.getInfoTypeForString('UNIT_ARTIST'),
						gc.getInfoTypeForString('UNIT_DOCTOR'),
						gc.getInfoTypeForString('UNIT_ENGINEER'),
						gc.getInfoTypeForString('UNIT_MERCHANT'),
						gc.getInfoTypeForString('UNIT_SCIENTIST'),
						gc.getInfoTypeForString('UNIT_SPY_GREAT')]

	GreatSpecialist  = [gc.getInfoTypeForString('SPECIALIST_GREAT_ARTIST'),
						gc.getInfoTypeForString('SPECIALIST_GREAT_DOCTOR'),
						gc.getInfoTypeForString('SPECIALIST_GREAT_ENGINEER'),
						gc.getInfoTypeForString('SPECIALIST_GREAT_MERCHANT'),
						gc.getInfoTypeForString('SPECIALIST_GREAT_SCIENTIST'),
						gc.getInfoTypeForString('SPECIALIST_GREAT_SPY'),
						gc.getInfoTypeForString('SPECIALIST_GREAT_PRIEST'),
						gc.getInfoTypeForString('SPECIALIST_GREAT_GENERAL')]

	PowerPriority	 = [gc.getInfoTypeForString('BUILDING_COAL_PLANT'),
						gc.getInfoTypeForString('BUILDING_GAS_PLANT'),
						gc.getInfoTypeForString('BUILDING_NUCLEAR_PLANT'),
						gc.getInfoTypeForString('BUILDING_HYDRO_PLANT'),
						gc.getInfoTypeForString('BUILDING_SOLAR_PLANT')]



class ExpandedCivicOptions:
	def __init__(self):
		self.ChoppingModifier					= gc.getInfoTypeForString('NO_CIVIC'), 50
		self.CombatVictoryWealth				= gc.getInfoTypeForString('NO_CIVIC')
		self.CorporationHappiness				= gc.getInfoTypeForString('CIVIC_SOCIAL_WELFARE')
		self.CorporationHealth					= gc.getInfoTypeForString('CIVIC_SUSTAINABILITY')
		self.ImprovedPlunder					= gc.getInfoTypeForString('CIVIC_TRIBALISM')
		self.ImprovedPillaging					= gc.getInfoTypeForString('CIVIC_TRIBALISM')
		self.NoEthnicDissent					= gc.getInfoTypeForString('CIVIC_MULTICULTURALISM')
		self.NoTradeRouteCulture				= gc.getInfoTypeForString('CIVIC_NATIONALISM')

		self.CorporationAppeal = [				(gc.getInfoTypeForString('CIVIC_AGRARIANISM'), gc.getInfoTypeForString('YIELD_FOOD'), 50),
												(gc.getInfoTypeForString('CIVIC_INDUSTRIALISM'), gc.getInfoTypeForString('YIELD_PRODUCTION'), 50),
												(gc.getInfoTypeForString('CIVIC_FREE_MARKET'), gc.getInfoTypeForString('YIELD_COMMERCE'), 50),
												(gc.getInfoTypeForString('CIVIC_RETRIBUTION'), 3, -50)]

		self.ExtraPalaceYield = [				(gc.getInfoTypeForString('NO_CIVIC'), gc.getInfoTypeForString('YIELD_COMMERCE'), 3)]

		self.FakeWonder = [						(gc.getInfoTypeForString('CIVIC_TRIBALISM'), gc.getInfoTypeForString('BUILDING_CIVIC_DEFENSE'))]



class ExpandedTraitOptions:
	def __init__(self):
		self.AttitudeChange =					gc.getInfoTypeForString('TRAIT_DIPLOMATIC'), 2
		self.CapitalBuildingModifier =			gc.getInfoTypeForString('TRAIT_TRADITIONAL'), -25
		self.CaptureResearch =					gc.getInfoTypeForString('TRAIT_IMPERIALIST')
		self.CivicDissentModifier =				gc.getInfoTypeForString('TRAIT_HUMANE'), -50
		self.CorporationExtraShare =			gc.getInfoTypeForString('TRAIT_FINANCIAL'), 25
		self.ExtraCargoSpace =					gc.getInfoTypeForString('TRAIT_ENTERPRISING')
		self.ExtraPopulation =					gc.getInfoTypeForString('TRAIT_EXPANSIVE'), 0 # this was also OP
		self.ExtraRoadSpeed =					gc.getInfoTypeForString('TRAIT_EXPANSIVE') # new ability improved road speed
		self.ExtraExperience =					gc.getInfoTypeForString('TRAIT_CHARISMATIC'), 1
		self.GreatTempleGoldenAge = 			gc.getInfoTypeForString('TRAIT_SPIRITUAL'), 100
		self.ImprovedPlunder =					gc.getInfoTypeForString('TRAIT_AGGRESSIVE')
		self.ImprovedPillaging =				gc.getInfoTypeForString('TRAIT_AGGRESSIVE')
		self.ImprovementUpgradeModifier =		gc.getInfoTypeForString('TRAIT_PROGRESSIVE'), -50
		self.MilitaryUnitUpgradeDiscount =		gc.getInfoTypeForString('TRAIT_TACTICAL'), -100
		self.NoResistance =						gc.getInfoTypeForString('TRAIT_IMPERIALIST')
		self.PillageImmunity =					gc.getInfoTypeForString('TRAIT_DEFENSIVE') # this ability is now used for partisans
		self.SpreadStateReligion = 				gc.getInfoTypeForString('TRAIT_SPIRITUAL')
		self.TradeRoutes =						gc.getInfoTypeForString('TRAIT_DIPLOMATIC'), 1

		self.AlwaysBuildCommerce = {			gc.getInfoTypeForString('PROCESS_WEALTH'): 			gc.getInfoTypeForString('TRAIT_FINANCIAL'),
												gc.getInfoTypeForString('PROCESS_RESEARCH'): 		gc.getInfoTypeForString('TRAIT_PHILOSOPHICAL'),
												gc.getInfoTypeForString('PROCESS_CULTURE'): 		gc.getInfoTypeForString('TRAIT_TRADITIONAL')}

# removing yields from culture because they are op
		self.CultureLevelYield = {				gc.getInfoTypeForString('YIELD_PRODUCTION'):		(gc.getInfoTypeForString('TRAIT_INDUSTRIOUS'), 0),
												gc.getInfoTypeForString('YIELD_COMMERCE'):			(gc.getInfoTypeForString('TRAIT_CREATIVE'), 0)}

		self.FreeBuildingClass = {				gc.getInfoTypeForString('TRAIT_DEFENSIVE'):			gc.getInfoTypeForString('BUILDINGCLASS_WALLS'),
												gc.getInfoTypeForString('TRAIT_MARTIAL'):			gc.getInfoTypeForString('BUILDINGCLASS_BARRACKS'),
												gc.getInfoTypeForString('TRAIT_INDUSTRIOUS'):			gc.getInfoTypeForString('BUILDINGCLASS_TANNERY'),
												gc.getInfoTypeForString('TRAIT_CREATIVE'):			gc.getInfoTypeForString('BUILDINGCLASS_KILN')}

		self.GreatPersonTypeModifier = {		gc.getInfoTypeForString('UNIT_ARTIST'): 			(gc.getInfoTypeForString('TRAIT_CREATIVE'),		 50),
												gc.getInfoTypeForString('UNIT_DOCTOR'):				(gc.getInfoTypeForString('TRAIT_HUMANE'),		 50),
												gc.getInfoTypeForString('UNIT_ENGINEER'): 			(gc.getInfoTypeForString('TRAIT_INDUSTRIOUS'),	 50),
												gc.getInfoTypeForString('UNIT_MERCHANT'): 			(gc.getInfoTypeForString('TRAIT_ENTERPRISING'),	 50),
												gc.getInfoTypeForString('UNIT_PROPHET'): 			(gc.getInfoTypeForString('TRAIT_SPIRITUAL'),	 50),
												gc.getInfoTypeForString('UNIT_SCIENTIST'):			(gc.getInfoTypeForString('TRAIT_PROGRESSIVE'),	 50),
												gc.getInfoTypeForString('UNIT_SPY_GREAT'):			(gc.getInfoTypeForString('TRAIT_DIPLOMATIC'),	 50)}

		self.FakeWonder = [						(gc.getInfoTypeForString('TRAIT_CHARISMATIC'), 		gc.getInfoTypeForString('BUILDING_TRAIT_CHARISMATIC')),
												(gc.getInfoTypeForString('TRAIT_FINANCIAL'), 		gc.getInfoTypeForString('BUILDING_TRAIT_FINANCIAL')),
												(gc.getInfoTypeForString('TRAIT_IMPERIALIST'), 		gc.getInfoTypeForString('BUILDING_TRAIT_IMPERIALIST')),
												(gc.getInfoTypeForString('TRAIT_JUDICIAL'), 		gc.getInfoTypeForString('BUILDING_TRAIT_JUDICIAL')),
												(gc.getInfoTypeForString('TRAIT_MARTIAL'), 			gc.getInfoTypeForString('BUILDING_TRAIT_MARTIAL')),
												(gc.getInfoTypeForString('TRAIT_ORGANIZED'), 		gc.getInfoTypeForString('BUILDING_TRAIT_ORGANIZED')),
												(gc.getInfoTypeForString('TRAIT_PHILOSOPHICAL'), 	gc.getInfoTypeForString('BUILDING_TRAIT_PHILOSOPHICAL')),
												(gc.getInfoTypeForString('TRAIT_POLITICAL'), 		gc.getInfoTypeForString('BUILDING_TRAIT_POLITICAL')),
												(gc.getInfoTypeForString('TRAIT_PROGRESSIVE'), 		gc.getInfoTypeForString('BUILDING_TRAIT_PROGRESSIVE'))]



class ExpandedUnitOptions:
	def __init__(self):							# Use for Unique Units only
		self.Capture 							= [gc.getInfoTypeForString('UNIT_CORSAIR')]
		self.Enslave 							= [gc.getInfoTypeForString('UNIT_EAGLE_WARRIOR'), gc.getInfoTypeForString('UNIT_BANDEIRANTE')]
		self.Fire		 						= [(gc.getInfoTypeForString('UNIT_FLAMETHROWER'), 5, 15, 5)]
		self.Incapacitate 						= [(gc.getInfoTypeForString('UNIT_BLOWGUNNER'), 2, 2)]

		self.ColonistFreeBuildingClass = [		gc.getInfoTypeForString('BUILDINGCLASS_BARRACKS'),
												gc.getInfoTypeForString('BUILDINGCLASS_GRANARY'),
												gc.getInfoTypeForString('BUILDINGCLASS_KILN'),
												gc.getInfoTypeForString('BUILDINGCLASS_TANNERY')]



class ExpandedBuildingOptions:
	def __init__(self):
		self.AllowFixedTenets					= gc.getInfoTypeForString('BUILDINGCLASS_SHWEDAGON_PAYA')
		self.AttitudeChange						= gc.getInfoTypeForString('BUILDINGCLASS_TAJ_MAHAL'), 1
		self.FreeGreatGeneral					= gc.getInfoTypeForString('BUILDINGCLASS_BRANDENBURG_GATE')
		self.GoldenAgeGPPModifier 				= gc.getInfoTypeForString('BUILDINGCLASS_NATIONAL_FESTIVAL'), 100
		self.HuntingModifier 					= gc.getInfoTypeForString('BUILDINGCLASS_NATURAL_WONDER_NGORONGORO'), 100
		self.RandomGreatPerson					= gc.getInfoTypeForString('BUILDINGCLASS_NAZCA_LINES')
		self.ReligionSharedGoldenAge			= gc.getInfoTypeForString('BUILDINGCLASS_CRISTO_REDENTOR'), 50
		self.WonderYield						= [(gc.getInfoTypeForString('BUILDINGCLASS_HOTEL'), YieldTypes.YIELD_COMMERCE, 2)]



class ExpandedImprovementOptions:
	def __init__(self):
		self.Polluting = [						(gc.getInfoTypeForString('IMPROVEMENT_MINE'), gc.getInfoTypeForString('BUILDINGCLASS_RECYCLING_CENTER')),
												(gc.getInfoTypeForString('IMPROVEMENT_WELL'), -1),
												(gc.getInfoTypeForString('IMPROVEMENT_OFFSHORE_PLATFORM'), -1),
												(gc.getInfoTypeForString('IMPROVEMENT_WORKSHOP'), gc.getInfoTypeForString('BUILDINGCLASS_RECYCLING_CENTER')),
												(gc.getInfoTypeForString('IMPROVEMENT_VILLAGE'), gc.getInfoTypeForString('BUILDINGCLASS_PUBLIC_TRANSPORTATION')),
												(gc.getInfoTypeForString('IMPROVEMENT_TOWN'), gc.getInfoTypeForString('BUILDINGCLASS_PUBLIC_TRANSPORTATION'))]



### SCRIPT DATA

def initPlayerData(pPlayer):
	'Initializes the scriptdata of a player'
	CivicList = []
	TenetList = []

	for iCategory in xrange(gc.getNumCivicOptionInfos()):
		if HR_Religion.Tenets().isTenetCategory(iCategory):
			iTenet = pPlayer.getCivics(iCategory)
			if iTenet == -1:
				iTenet = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationInitialCivics(iCategory)
			TenetList.append(iTenet)

		else:
			iCivic = pPlayer.getCivics(iCategory)
			if iCivic == -1:
				iCivic = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationInitialCivics(iCategory)
			CivicList.append(iCivic)

	CivicData = ""
	for iCivic in CivicList:
		CivicData += str(iCivic)
		CivicData += ","
	CivicData = CivicData[:-1]

	TenetData = ""
	for iTenet in TenetList:
		TenetData += str(iTenet)
		TenetData += ","
	TenetData = TenetData[:-1]

	ReligionData = str(pPlayer.getStateReligion() + 1)
	FaithData = "0" + "/" + str(HR_Religion.Faith().iThresholdIncrease)
	ReformationData = "0"
	AnarchyData = "0"

	ShareData = ""
	TradeData = ""
	for iOrganization in xrange(gc.getNumCorporationInfos()):
		if gc.getCorporationInfo(iOrganization).getSpreadCost() > 0:
			ShareData += "0,"
			TradeData += "0,"
	ShareData = ShareData[:-1]
	TradeData = TradeData[:-1]

	PlayerData = CivicData + ":" + TenetData + ":" + ReligionData + ":" + FaithData + ":" + ReformationData + ":" + AnarchyData + ":" + ShareData + ":" + TradeData
	pPlayer.setScriptData(PlayerData)



def getPlayerData(pPlayer, iSection):
	'Returns the desired section of player scriptdata'
	PlayerData = pPlayer.getScriptData().split(":")
	return PlayerData[iSection]



def setPlayerData(pPlayer, iSection, sData):
	'Sets the a section of player scriptdata to desired string'
	PlayerData = pPlayer.getScriptData().split(":")
	newPlayerData = ""
	PlayerData[iSection] = sData
	for i in xrange(len(PlayerData)):
		newPlayerData += PlayerData[i]
		if len(PlayerData) - 1 != i:
			newPlayerData += ":"

	pPlayer.setScriptData(newPlayerData)



def initCityData(pCity, Name):
	'Initializes the scriptdata of a city'

	# CITY_ID
	if Name == "":
		Name = HR_Cities.findCityKey(pCity.getName())

	CityData = Name
	CityData += ":"

	# GREAT_PEOPLE_PROGRESS
	GPData = ""
	for iGP in GreatPeople:
		GPData += "0"
		if iGP != GreatPeople[-1]:
			GPData += ","

	CityData += GPData
	CityData += ":"

	# DISSENT
	CityData += str(CivilWar.CivilWar().iStartDissent)
	CityData += ":"

	# CULTURE_LEVEL
	CityData += str(pCity.getCultureLevel())
	CityData += ":"

	# CORPORATE_HAPPINESS
	CityData += "0"
	CityData += ":"

	# CORPORATE_HEALTH
	CityData += "0"
	CityData += ":"

	# CORPORATE_YIELD
	CityData += "000"
	CityData += ":"

	# STARVATION
	CityData += "0"

	pCity.setScriptData(CityData)



def getCityData(pCity, iSection):
	'Returns the desired section of city scriptdata'
	if pCity.getScriptData() == "":
		initCityData(pCity, "")

	CityData = pCity.getScriptData().split(":")
	return CityData[iSection]



def setCityData(pCity, iSection, sData):
	'Sets the a section of city scriptdata to desired string'
	if pCity.getScriptData() == "":
		initCityData(pCity, "")

	CityData = pCity.getScriptData().split(":")
	newCityData = ""
	CityData[iSection] = sData
	for i in xrange(len(CityData)):
		newCityData += CityData[i]
		if len(CityData) - 1 != i:
			newCityData += ":"

	pCity.setScriptData(newCityData)



def getPlotData(pPlot, iSection):
	'Returns the desired section of plot scriptdata'
	if pPlot.getScriptData() == "":
		return ""

	PlotData = pPlot.getScriptData().split(":")
	return PlotData[iSection]



def setPlotData(pPlot, iSection, sData):
	'Sets the a section of plot scriptdata to desired string'
	PlotData = pPlot.getScriptData().split(":")
	newPlotData = ""
	PlotData[iSection] = sData
	for i in xrange(len(PlotData)):
		newPlotData += PlotData[i]
		if len(PlotData) - 1 != i:
			newPlotData += ":"

	pPlot.setScriptData(newPlotData)



def doDataChecks(pPlayer, bNewPlayer):
	'Checks if civics/tenets/religions/etc have changed and triggers appropriate events'
	if bNewPlayer:
		initPlayerData(pPlayer)

	OldCivicList = getCivicData(pPlayer)
	NewCivicList = []
	OldTenetList = HR_Religion.Tenets().getTenetData(pPlayer)
	NewTenetList = []

	bReformation = False
	for iCategory in xrange(gc.getNumCivicOptionInfos()):
		if HR_Religion.Tenets().isTenetCategory(iCategory):
			iOldTenet = OldTenetList[iCategory - len(OldCivicList)]
			iNewTenet = pPlayer.getCivics(iCategory)
			NewTenetList.append(iNewTenet)
			if bNewPlayer or iOldTenet != iNewTenet:
				HR_Religion.Tenets().onTenetChanged(pPlayer, iOldTenet, False)
				HR_Religion.Tenets().onTenetChanged(pPlayer, iNewTenet, True)
				bReformation = True
		else:
			iOldCivic = OldCivicList[iCategory]
			iNewCivic = pPlayer.getCivics(iCategory)
			NewCivicList.append(iNewCivic)
			if bNewPlayer or iOldCivic != iNewCivic:
				onCivicChanged(pPlayer, iOldCivic, False)
				onCivicChanged(pPlayer, iNewCivic, True)

	iLastReligion = int(getPlayerData(pPlayer, PlayerData.index('STATE_RELIGION')))
	iStateReligion = pPlayer.getStateReligion() + 1
	if iStateReligion != iLastReligion:
		bReformation = True
		if iStateReligion == 0 and iLastReligion > 0:
			iStateReligion = iLastReligion * -1
		setPlayerData(pPlayer, PlayerData.index('STATE_RELIGION'), str(iStateReligion))

	if bReformation:
		HR_Religion.setReligiousAttitude(pPlayer)

	iReformationTimer = HR_Religion.Tenets().getReformationTimer(pPlayer)
	if iReformationTimer > 0:
		HR_Religion.Tenets().setReformationTimer(pPlayer, iReformationTimer - 1)
	elif iReformationTimer == -1:
		HR_Religion.Tenets().setReformationTimer(pPlayer, 0)

	if not bNewPlayer:
		setCivicData(pPlayer, NewCivicList)
		HR_Religion.Tenets().setTenetData(pPlayer, NewTenetList)



### CIVICS

def getCivicData(pPlayer):
	''
	CivicList = []
	CivicData = getPlayerData(pPlayer, PlayerData.index('CIVICS')).split(",")
	for szData in CivicData:
		CivicList.append(int(szData))

	return CivicList



def setCivicData(pPlayer, CivicList):
	''
	CivicData = ""
	for iCivic in CivicList:
		CivicData += str(iCivic)
		CivicData += ","
	CivicData = CivicData[:-1]

	setPlayerData(pPlayer, PlayerData.index('CIVICS'), CivicData)



def onCivicChanged(pPlayer, iCivic, bAdopted):
	'Event triggered when a specified civic has been changed for a player'

	# Extra Palace Yield
	for eCivic, YieldType, iYieldChange in Civic.ExtraPalaceYield:
		if iCivic == eCivic:
			pCapital = pPlayer.getCapitalCity()
			pCapital.setBuildingYieldChange(gc.getInfoTypeForString('BUILDINGCLASS_PALACE'), YieldType, bAdopted * iYieldChange)

	# Fake Wonders
	for eCivic, iBuilding in Civic.FakeWonder:
		if iCivic == eCivic:
			pCapital = pPlayer.getCapitalCity()
			pCapital.setNumRealBuilding(iBuilding, bAdopted)

	# Corporations
	if pPlayer.countTotalHasCorporation() > 0:
		(loopCity, i) = pPlayer.firstCity(False)
		while(loopCity):
			HR_Organizations.updateCityOrganizations(loopCity)
			(loopCity, i) = pPlayer.nextCity(i, False)



### COMBAT

def doCombatCommerce(pPlayer, pUnit, pPlot, iCommerceType):
	'Grants commerce when a unit is defeated'

	# Determine commerce value from dead unit's experience
	iReward = max(1, pUnit.getExperience())

	# Wealth
	if iCommerceType == 0:
		pPlayer.changeGold(iReward)
		sRecipient = "You earn"
		sIcon = "[ICON_GOLD]"

	# Culture
	elif iCommerceType == 2:
		pCity = gc.getMap().findCity(pPlot.getX(), pPlot.getY(), pPlayer.getID(), TeamTypes.NO_TEAM, True, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
		pCity.changeCulture(pPlayer.getID(), iReward, True)
		sRecipient = pCity.getName() + " earns"
		sIcon = "[ICON_CULTURE]"

	# Other Commerces NYI
	else:
		return

	# Message player
	sUnit = pUnit.getName()
	if gc.getUnitInfo(pUnit.getUnitType()).isHiddenNationality():
		sAdj = ""
	else:
		sAdj = gc.getPlayer(pUnit.getOwner()).getCivilizationAdjective(0)

	CyInterface().addMessage(pPlayer.getID(), True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText('TXT_KEY_MESSAGE_COMBAT_COMMERCE', (sRecipient, iReward, sIcon, sAdj, sUnit)), None, 2, None, ColorTypes(gc.getInfoTypeForString('COLOR_WHITE')), 0, 0, False, False)



### CULTURE

def getCityCulture(pCity):
	'Gets culture level from city scriptdata'
	'Used to detect changes in culture level'
	return int(getCityData(pCity, CityData.index('CULTURE_LEVEL')))



def setCityCulture(pCity, iLevel):
	'Stores culture level in city scriptdata'
	'Used to detect changes in culture level'
	setCityData(pCity, CityData.index('CULTURE_LEVEL'), str(iLevel))



def getCultureTransfer(pImportCity, pExportCity):
	''
	pImportPlayer = gc.getPlayer(pImportCity.getOwner())
	pExportPlayer = gc.getPlayer(pExportCity.getOwner())

	iCultureTransfer = 0
	if not pImportPlayer.isCivic(Civic.NoTradeRouteCulture) and not pExportPlayer.isCivic(Civic.NoTradeRouteCulture):
		iImportPercent = pImportPlayer.getCommercePercent(CommerceTypes.COMMERCE_CULTURE)
		iExportPercent = pExportPlayer.getCommercePercent(CommerceTypes.COMMERCE_CULTURE)
		if not pImportPlayer.isHuman():
			iImportPercent += (CyGame().getHandicapType() * 3)
		if not pExportPlayer.isHuman():
			iExportPercent += (CyGame().getHandicapType() * 3)

		iExportPercent -= iImportPercent
		if iExportPercent > 0:
			iCultureTransfer = pExportCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE) * iExportPercent / 100

			iImportCitySize = pImportCity.getPopulation()
			iExportCitySize = pExportCity.getPopulation()
			if iExportCitySize > iImportCitySize:
				iCultureTransfer *= iImportCitySize / iExportCitySize

			iTurns = CyGame().getGameTurn() - pImportCity.getGameTurnAcquired()
			iModifier = -100 + min(100, iTurns * 100 / CivilWar.CivilWar().iEscalationTurns)
			iCultureTransfer += ((iCultureTransfer * iModifier) / 100)

	return iCultureTransfer



def getLiberationChance(pCity):
	''
	fLiberation = 0.0
	pPlot = pCity.plot()
	iCulturalOwner = pPlot.calculateCulturalOwner()

	if iCulturalOwner > -1:
		if gc.getPlayer(iCulturalOwner).getTeam() != pCity.getTeam():
			iCityStrength = pCity.cultureStrength(iCulturalOwner)
			iGarrisonStrength = pCity.cultureGarrison(iCulturalOwner)

			if iCityStrength > iGarrisonStrength:
				iBestModifier = 0
				for iUnit in xrange(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(iUnit)
					if not pUnit.isNone() and not pUnit.isDead():
						iRevoltProtection = pUnit.getRevoltProtection()
						if iRevoltProtection > iBestModifier:
							iBestModifier = iRevoltProtection

				fCityStrength = float(iCityStrength)
				fGarrisonStrength = float(iGarrisonStrength)
				fProbability = float(gc.getDefineINT('REVOLT_TEST_PROB') * (100 - min(iBestModifier, 100)) / 100)

				if BugPath.isMac():
					# BTS calculation
					fLiberation = (1.0 - (fGarrisonStrength / fCityStrength)) * min(100.0, fProbability)

				else:
					# K-Mod calculation
					fVictoryDelay = float(gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getVictoryDelayPercent())
					fLiberation = (fCityStrength - fGarrisonStrength) / (fCityStrength + 2 * fGarrisonStrength) * (fProbability / fVictoryDelay)

	return fLiberation



def getCityEthnicityHelp(pCity):
	'Displays help text for the city ethnicity bar'
	lNationalities = []
	for iPlayer in xrange(gc.getMAX_PLAYERS()):
		if gc.getPlayer(iPlayer).isAlive():
			iPercent = pCity.plot().calculateCulturePercent(iPlayer)
			if iPercent > 0:
				lNationalities.append((iPercent, iPlayer))

	szHelp = "Ethnicity:"
	lNationalities.sort()
	lNationalities.reverse()
	for iPercent, iPlayer in lNationalities:
		pPlayer = gc.getPlayer(iPlayer)
		szColor = "<color=%d,%d,%d,%d>" % (pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA())
		szCiv = szColor + pPlayer.getCivilizationAdjective(0) + "</color>"
		szSpace = u""
		if len(str(iPercent)) == 1:
			szSpace = u" "
		szHelp += u"\n%s%d%% %s" % (szSpace, iPercent, szCiv)

	fLiberation = getLiberationChance(pCity)
	if fLiberation > 0.0:
		szHelp += u"\n\Revolt Chance: %.2f%%" % fLiberation

	return szHelp



### GREAT PEOPLE & SPECIALISTS

def getGreatPersonProgress(pCity, iUnit):
	'Returns the GPP progress a city has towards the specified Great Person'
	if pCity:
		GPProgress = getCityData(pCity, CityData.index('GREAT_PEOPLE_PROGRESS')).split(",")
		if len(GPProgress) == len(GreatPeople):
			if iUnit in GreatPeople:
				i = GreatPeople.index(iUnit)
				return int(GPProgress[i])

	return 0



def getGreatPersonRate(pCity, iUnit):
	'Returns the modified rate at which a city generates GPP for the specified Great Person'
	if pCity:
		if iUnit in GreatPeople:
			iModifier = getGreatPersonModifier(pCity, iUnit)
			iRate = pCity.getGreatPeopleUnitRate(iUnit)
			iRate += ((iRate * iModifier) / 100)
			return iRate

	return -1



def getGreatPersonModifier(pCity, iUnit):
	'Returns the total modifier for generation of a specified Great Person in a city'
	pPlayer = gc.getPlayer(pCity.getOwner())
	iModifier = pPlayer.getGreatPeopleRateModifier() + pCity.getGreatPeopleRateModifier()

	if iUnit in Trait.GreatPersonTypeModifier.keys():
		iTrait, iTraitModifier = Trait.GreatPersonTypeModifier[iUnit]
		if pPlayer.hasTrait(iTrait):
			iModifier += iTraitModifier

	iBuildingClass, iGoldenAgeModifier = Building.GoldenAgeGPPModifier
	if pPlayer.isGoldenAge() and pPlayer.getBuildingClassCount(iBuildingClass) > 0:
		iModifier += iGoldenAgeModifier

	iStateReligion = pPlayer.getStateReligion()
	if iStateReligion > -1:
		iTenet, iTenetModifier = HR_Religion.Tenets().TempleGPPModifier
		if pPlayer.isCivic(iTenet):
			iBuilding = HR_Religion.getReligionTemple(iStateReligion)
			if pCity.getNumBuilding(iBuilding) > 0:
				iModifier += iTenetModifier

	iTenet, iStateModifier, iNonStateModifier = HR_Religion.Tenets().StateReligionGPPModifier
	if pPlayer.isCivic(iTenet):
		for iReligion in xrange(gc.getNumReligionInfos()):
			if pCity.isHasReligion(iReligion):
				if iReligion == pPlayer.getStateReligion():
					iModifier += iStateModifier
				else:
					iModifier += iNonStateModifier

	if iUnit in HR_Religion.Tenets().GreatPersonTypeModifier.keys():
		iTenet, iTenetModifier = HR_Religion.Tenets().GreatPersonTypeModifier[iUnit]
		if pPlayer.isCivic(iTenet):
			iModifier += iTenetModifier

	if pCity.isHolyCityByType(pPlayer.getStateReligion()):
		iTenet, iTenetModifier = HR_Religion.Tenets().ShrineGPPModifier
		if pPlayer.isCivic(iTenet):
			iModifier += iTenetModifier

	return iModifier



def getGreatPersonTurns(pCity, iUnit):
	'Returns the number of turns in which a city will generate the specified Great Person'
	if pCity:
		iThreshold = gc.getPlayer(pCity.getOwner()).greatPeopleThreshold(False)
		iProgress = getGreatPersonProgress(pCity, iUnit)
		iRate = getGreatPersonRate(pCity, iUnit)
		if iRate > 0:
			iTurns = (iThreshold - iProgress + iRate - 1) / iRate
			return iTurns

	return -1



def getGreatPersonTopCities(pPlayer, iMaxCities):
	'Returns a list of cities closest to generating a Great Person'
	'Returns Great Person progression by type for the currently selected city'
	GPCityList = []
	pHeadSelectedCity = CyInterface().getHeadSelectedCity()

	if pHeadSelectedCity and pHeadSelectedCity.getTeam() == CyGame().getActiveTeam():
		iMaxCities = len(GreatPeople)
		for iGP in GreatPeople:
			iTurns = getGreatPersonTurns(pHeadSelectedCity, iGP)
			if iTurns > -1:
				GPCityList.append((iTurns, iGP, pHeadSelectedCity))

	else:
		(loopCity, i) = pPlayer.firstCity(False)
		while(loopCity):
			for iGP in GreatPeople:
				iTurns = getGreatPersonTurns(loopCity, iGP)
				if iTurns > -1:
					GPCityList.append((iTurns, iGP, loopCity))
			(loopCity, i) = pPlayer.nextCity(i, False)

	if GPCityList:
		GPCityList.sort()
		if len(GPCityList) > iMaxCities:
			del GPCityList[iMaxCities:]

	return GPCityList



def getGreatPersonBarHelp(pPlayer):
	'Provides help text for main interface Great Person bar'
	szHelp = u""
	GPCityList = getGreatPersonTopCities(pPlayer, 5)

	if GPCityList:
		sColor = "<color=%d,%d,%d,%d>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA())
		szHelp += "<font=2>" + CyTranslator().getText('TXT_KEY_INTERFACE_GREAT_PEOPLE_HELP_HEADER', ())
		iThreshold = pPlayer.greatPeopleThreshold(False)
		for iTurns, iGP, pCity in GPCityList:
			iProgress = getGreatPersonProgress(pCity, iGP)
			szHelp += "\n\n" + getGreatPersonSymbol(iGP) + gc.getUnitInfo(iGP).getDescription() + "\n"
			szHelp += sColor + pCity.getName() + "</color>" + ": " + CyTranslator().getText('TXT_KEY_INTERFACE_GREAT_PEOPLE_HELP_TURNS', (iProgress, iThreshold, iTurns))
		szHelp += "</font>"

	return szHelp



def getGreatPersonCityBarHelp(pCity, iUnit):
	'Provides help text for Great Person bar tooltips'
	pPlayer = gc.getPlayer(pCity.getOwner())
	iProgress = getGreatPersonProgress(pCity, iUnit)
	iThreshold = pPlayer.greatPeopleThreshold(False)
	iSpecialist, iSpecialistRate = getGreatPersonSpecialistInfo(iUnit)
	iNumSpecialists = pCity.getSpecialistCount(iSpecialist) + pCity.getFreeSpecialistCount(iSpecialist)
	iSpecialistRate *= iNumSpecialists

	iBuildingCount = 0
	iBuildingRate = 0
	for iBuilding in xrange(gc.getNumBuildingInfos()):
		if pCity.getNumBuilding(iBuilding) > 0:
			if gc.getBuildingInfo(iBuilding).getGreatPeopleUnitClass() == gc.getUnitInfo(iUnit).getUnitClassType():
				iBuildingCount += 1
				iBuildingRate += gc.getBuildingInfo(iBuilding).getGreatPeopleRateChange()

	iModifier = getGreatPersonModifier(pCity, iUnit)
	iModAmount = ((iSpecialistRate + iBuildingRate) * iModifier) / 100

	GPChar = CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR)
	szBullet = u"%c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)
	szHelp = CyTranslator().changeTextColor(gc.getUnitInfo(iUnit).getDescription(), gc.getInfoTypeForString('COLOR_GREAT_PEOPLE_RATE'))
	szHelp += u"\n%d of %d%c" % (iProgress, iThreshold, GPChar)

	if iSpecialistRate > 0 or iBuildingRate > 0:
		if iSpecialistRate > 0:
			szHelp += u"\n%s+%d%c from Specialists" % (szBullet, iSpecialistRate, GPChar)
		if iBuildingRate > 0:
			szHelp += u"\n%s+%d%c from Wonders (%d)" % (szBullet, iBuildingRate, GPChar, iBuildingCount)

		if iModifier > 0:
			szHelp += u"\n%s+%d%c from Modifier (%d%%)" % (szBullet, iModAmount, GPChar, iModifier)
		elif iModifier < 0:
			szHelp += u"\n%s%d%c from Modifier (%d%%)" % (szBullet, iModAmount, GPChar, iModifier)

	return szHelp



def getGreatPersonSymbol(iUnit):
	'Returns the appropriate symbol as a string'
	if iUnit == GreatPeople[0]:		sIcon = "[ICON_CULTURE]"
	elif iUnit == GreatPeople[1]:	sIcon = "[ICON_HEALTHY]"
	elif iUnit == GreatPeople[2]:	sIcon = "[ICON_PRODUCTION]"
	elif iUnit == GreatPeople[3]:	sIcon = "[ICON_GOLD]"
	elif iUnit == GreatPeople[4]:	sIcon = "[ICON_RESEARCH]"
	elif iUnit == GreatPeople[5]:	sIcon = "[ICON_ESPIONAGE]"
	else:							sIcon = "[ICON_GREATPEOPLE]"
	return CyTranslator().getText(sIcon, ())



def getGreatPersonSpecialistType(iGP, bGreat):
	'Returns the specialist ID associated with the specified Great Person'
	iUnitClass = gc.getUnitInfo(iGP).getUnitClassType()
	for iSpecialist in xrange(gc.getNumSpecialistInfos()):
		SpecialistInfo = gc.getSpecialistInfo(iSpecialist)
		if SpecialistInfo.getGreatPeopleUnitClass() == iUnitClass:
			if bGreat:
				iSpecialist = gc.getInfoTypeForString(SpecialistInfo.getType().replace("_", "_GREAT_"))
			return iSpecialist

	return -1



def getGreatPersonSpecialistInfo(iUnit):
	'Returns the specialist ID and GPP rate associated with the specified Great Person'
	iUnitClass = gc.getUnitInfo(iUnit).getUnitClassType()
	for iSpecialist in xrange(gc.getNumSpecialistInfos()):
		if gc.getSpecialistInfo(iSpecialist).getGreatPeopleUnitClass() == iUnitClass:
			iRate = gc.getSpecialistInfo(iSpecialist).getGreatPeopleRateChange()
			return iSpecialist, iRate

	return -1, -1



def getGreatGeneralBarHelp(pPlayer):
	''
	iCombatExp = pPlayer.getCombatExperience()
	iThreshold = pPlayer.greatPeopleThreshold(True)
	szUnit = gc.getUnitInfo(gc.getInfoTypeForString('UNIT_GENERAL')).getDescription()
	szText = CyTranslator().getText('TXT_KEY_INTERFACE_GREAT_GENERAL_BAR_HELP', (szUnit, iCombatExp, iThreshold))

	return szText



def getSpecialistHelp(iSpecialist):
	'Provides extra information for specialist tooltips'
	szHelp = CyGameTextMgr().getSpecialistHelp(iSpecialist, False).replace("Birth Rate", "")

	if iSpecialist == gc.getInfoTypeForString('SPECIALIST_PRIEST'):
		szHelp = szHelp.replace(u"%c" % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR), u"%c" % CyGame().getSymbolID(FontSymbols.RELIGION_CHAR))

	if iSpecialist != gc.getInfoTypeForString('SPECIALIST_CITIZEN'):
		pCity = CyInterface().getHeadSelectedCity()
		if pCity:
			iActive = pCity.getSpecialistCount(iSpecialist)
			iFree = pCity.getFreeSpecialistCount(iSpecialist)
			iTotal = pCity.getMaxSpecialistCount(iSpecialist)
			if iTotal > 0:
				szHelp += CyTranslator().getText('TXT_KEY_INTERFACE_CITY_SPECIALIST_HELP_1', (iActive, iTotal))
			if iFree > 0:
				szHelp += CyTranslator().getText('TXT_KEY_INTERFACE_CITY_SPECIALIST_HELP_2', (iFree, ))

	return szHelp

	

### MISSIONS

def doGreatPeopleMissions(pUnit, iData1, iData2):
	''
	iPlayer = pUnit.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iReligion = pPlayer.getStateReligion()

	pPlot = pUnit.plot()
	pCity = pPlot.getPlotCity()
	iPlotOwner = pPlot.getOwner()
	if iPlotOwner > -1:
		pPlotOwner = gc.getPlayer(iPlotOwner)
		iPlotTeam = pPlotOwner.getTeam()
		pPlotTeam = gc.getTeam(iPlotTeam)

	pUnit.kill(False, -1)

	# Propaganda (Artist)
	if iData1 == 901:
		for iTeamX in xrange(gc.getMAX_CIV_TEAMS()):
			pTeam.setWarWeariness(iTeamX, 0)

	# Inoculation (Doctor)
	elif iData1 == 911:
		pass

	# Humanitarian (Doctor)
	elif iData1 == 912:
		for iPlayerX in xrange(gc.getMAX_CIV_PLAYERS()):
			pPlayerX = gc.getPlayer(iPlayerX)
			iTeamX = pPlayerX.getTeam()
			if pPlayerX.isAlive() and pTeam.isHasMet(pPlayerX.getTeam()) and iTeamX != iTeam:
				pPlayerX.AI_changeAttitudeExtra(iPlayer, 1)

	# Resupply (Engineer)
	elif iData1 == 921:
		(loopUnit, iter) = pPlayer.firstUnit(False)
		while(loopUnit):
			loopUnit.setMadeAttack(False)
			loopUnit.setMoves(0)
			(loopUnit, iter) = pPlayer.nextUnit(iter, False)

	# Expedition (Merchant)
	elif iData1 == 931:
		pass

	# Pilgrimage (Prophet)
	elif iData1 == 941:
		pass

	# Mediation (Prophet)
	elif iData1 == 942:
		for iPlayerX in xrange(gc.getMAX_CIV_PLAYERS()):
			pPlayerX = gc.getPlayer(iPlayerX)
			iTeamX = pPlayerX.getTeam()
			if pPlayerX.isAlive() and pTeam.isHasMet(pPlayerX.getTeam()) and iTeamX != iTeam:
				pPlayerX.forcePeace(iPlayer)


	# Encyclopedia (Scientist)
	elif iData1 == 951:
		for iTech in xrange(gc.getNumTechInfos()):
			if pTeam.isHasTech(iTech):
				continue
			iResearch = min(pTeam.getResearchCost(iTech) / 5, pTeam.getResearchLeft(iTech))
			for iTeamX in xrange(gc.getMAX_CIV_TEAMS()):
				pTeamX = gc.getTeam(iTeamX)
				if pTeam.isHasMet(iTeamX) and pTeamX.isAlive():
					if pTeamX.isHasTech(iTech):
						pTeam.changeResearchProgress(iTech, iResearch, iPlayer)
						break

	# Mystery (Scientist)
	elif iData1 == 952:
		pass


	# Coup (Spy)
	elif iData1 == 961:
		pass

	# Rally (General)
	elif iData1 == 971:
		pass



### POLLUTION

def hasPollution(pPlot):
	'Returns true if tile is polluted'
	iFeature = pPlot.getFeatureType()
	if iFeature > -1:
		if gc.getFeatureInfo(iFeature).getType().startswith('FEATURE_POLLUTION'):
			return True
	return False



def addPollution(pPlot):
	'Adds the appropriate type of pollution to a tile'
	iFeature = pPlot.getFeatureType()
	if iFeature == gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS'):
		pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_POLLUTION_FLOOD_PLAINS'), 1)
	elif iFeature == gc.getInfoTypeForString('FEATURE_FOREST') or iFeature == gc.getInfoTypeForString('FEATURE_JUNGLE') or iFeature == gc.getInfoTypeForString('FEATURE_SAVANNAH'):
		lNearbyCities = listCitiesInRange(pPlot.getX(), pPlot.getY())
		if len(lNearbyCities) > 0:
			for pCity in lNearbyCities:
				if pCity.getOwner() == pPlot.getOwner():
					doChopping(pPlot, pCity, True)
					break
		pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_POLLUTION'), 1)

	else:
		pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_POLLUTION'), 1)



def removePollution(pPlot):
	'Removes pollution and restores a tile appropriately'
	iFeature = pPlot.getFeatureType()
	if iFeature == gc.getInfoTypeForString('FEATURE_POLLUTION_FLOOD_PLAINS'):
		pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS'), 1)
	else:
		pPlot.setFeatureType(-1, 1)



### TERRAIN

def doChopping(pPlot, pCity, bForce):
	'Adds production from chopping to a city'
	iPlayer = pCity.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iFeature = pPlot.getFeatureType()
	lFeature = [gc.getInfoTypeForString('FEATURE_FOREST'), gc.getInfoTypeForString('FEATURE_JUNGLE'), gc.getInfoTypeForString('FEATURE_SAVANNAH')]
	lBuild = [gc.getInfoTypeForString('BUILD_REMOVE_FOREST'), gc.getInfoTypeForString('BUILD_REMOVE_JUNGLE'), gc.getInfoTypeForString('BUILD_REMOVE_SAVANNAH')]
	iProduction = 0
	iBaseProduction = 0

	for i in xrange(len(lFeature)):
		if lFeature[i] == iFeature:
			iBuild = lBuild[i]
			iBaseProduction = pPlot.getFeatureProduction(iBuild, pPlayer.getTeam(), pCity)
			break

	if iBaseProduction > 0:
		if bForce:
			iProduction += iBaseProduction

		# Extra chop production from civic
		if pPlayer.isCivic(Civic.ChoppingModifier[0]):
			iProduction += (iBaseProduction * Civic.ChoppingModifier[1] / 100)

		# Extra production if a Prime Timber resource is also chopped
		if pPlot.getBonusType(-1) == gc.getInfoTypeForString('BONUS_TIMBER'):
			pPlot.setBonusType(-1)
			iProduction += iBaseProduction
			if pPlayer.isCivic(Civic.ChoppingModifier[0]):
				iProduction += (iBaseProduction * Civic.ChoppingModifier[1] / 100)

			BonusInfo = gc.getBonusInfo(gc.getInfoTypeForString('BONUS_TIMBER'))
			for iPlayerX in xrange (gc.getMAX_CIV_PLAYERS()):
				if iPlayerX != iPlayer:
					pPlayerX = gc.getPlayer(iPlayerX)
					if pPlot.isVisible(pPlayerX.getTeam(), False):
						CyInterface().addMessage(iPlayerX, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_MESSAGE_BONUS_DESTROYED", (BonusInfo.getDescription(),)), "", 0, BonusInfo.getButton(), gc.getInfoTypeForString("COLOR_WARNING_TEXT"), pPlot.getX(), pPlot.getY(), True, True)

	if iProduction > 0:
		sFeature = gc.getFeatureInfo(iFeature).getDescription()
		pCity.setFeatureProduction(iProduction + pCity.getFeatureProduction())
		CyInterface().addMessage(iPlayer, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_MISC_CLEARING_FEATURE_BONUS", (sFeature, iProduction, pCity.getName())), "", 0, "", -1, -1, -1, False, False)



### UTILITIES

def getAdvisorString(iBuilding):
	''
	iAdvisor = gc.getBuildingInfo(iBuilding).getAdvisorType()

	if iAdvisor == 0:
		return "Military"
	elif iAdvisor == 1:
		return "Religious"
	elif iAdvisor == 2:
		return "Economy"
	elif iAdvisor == 3:
		return "Science"
	elif iAdvisor == 4:
		return "Culture"
	elif iAdvisor == 5:
		return "Growth"

	return ""



def getPlayerBuilding(pPlayer, iBuildingClass):
	''
	iCivilization = pPlayer.getCivilizationType()
	if iCivilization == -1:
		return -1

	iBuilding = gc.getCivilizationInfo(iCivilization).getCivilizationBuildings(iBuildingClass)
	if iBuilding == -1:
		iBuilding = gc.getBuildingClassInfo(iBuildingClass).getDefaultBuildingIndex()

	return iBuilding



def getPlayerUnit(pPlayer, iUnitClass):
	''
	iCivilization = pPlayer.getCivilizationType()
	if iCivilization == -1:
		return -1

	iUnit = gc.getCivilizationInfo(iCivilization).getCivilizationUnits(iUnitClass)
	if iUnit == -1:
		iUnit = gc.getUnitClassInfo(iUnitClass).getDefaultUnitIndex()

	return iUnit



def getUnitCategory(iUnit):
	'0 = Unit'
	'1 = Military Unit'
	'2 = Unique Unit'

	UnitInfo = gc.getUnitInfo(iUnit)
	UnitClassInfo = gc.getUnitClassInfo(UnitInfo.getUnitClassType())
	iDefaultUnit = UnitClassInfo.getDefaultUnitIndex()

	if UnitInfo.isGraphicalOnly():
		return -1
	elif iDefaultUnit > -1 and iDefaultUnit != iUnit:
		return 2
	elif UnitInfo.getCombat() > 0 or UnitInfo.getAirCombat() > 0 or UnitInfo.isSuicide():
		if not UnitInfo.isAnimal() and not UnitInfo.isFound():
			return 1

	return 0



def getBuildingCategory(iBuilding):
	'0 = Building'
	'1 = Unique Building'
	'2 = Religious Building'
	'3 = Religious Wonder'
	'4 = National Wonder'
	'5 = Unique Wonder'
	'6 = World Wonder'
	'7 = Natural Wonder'
	'8 = Corporate Headquarters'

	BuildingInfo = gc.getBuildingInfo(iBuilding)
	if BuildingInfo.getType().find("_NATURAL_WONDER_") > 0:
		return 7
	elif BuildingInfo.getArtDefineTag() == "ART_DEF_BUILDING_FAKE" or BuildingInfo.isGraphicalOnly():
		return -1
	elif BuildingInfo.getReligionType() > -1:
		if isWorldWonderClass(BuildingInfo.getBuildingClassType()):
			return 3
		else:
			return 2
	elif BuildingInfo.getFoundsCorporation() > -1:
		return 8
	elif isWorldWonderClass(BuildingInfo.getBuildingClassType()):
		return 6
	else:
		iBuildingClass = BuildingInfo.getBuildingClassType()
		iDefaultBuilding = gc.getBuildingClassInfo(iBuildingClass).getDefaultBuildingIndex()
		if isNationalWonderClass(iBuildingClass):
			if iDefaultBuilding > -1 and iDefaultBuilding != iBuilding:
				return 5
			else:
				return 4
		else:
			if iDefaultBuilding > -1 and iDefaultBuilding != iBuilding:
				return 1
			else:
				return 0



def getBuildingHelp(iBuilding, bCivilopedia, pCity):
	''
	BuildingInfo = gc.getBuildingInfo(iBuilding)
	szHelp = CyGameTextMgr().getBuildingHelp(iBuilding, bCivilopedia, False, False, pCity)
	PrefixList = []
	SuffixList = []

	# Dissent
	iBuildingClass = BuildingInfo.getBuildingClassType()
	if iBuildingClass in CivilWar.CivilWar().BuildingClassModifiers.keys():
		PrefixList.append(CyTranslator().getText("TXT_KEY_BUILDING_DISSENT_MODIFIER", (CivilWar.CivilWar().BuildingClassModifiers[iBuildingClass], )))
	elif iBuilding in CivilWar.CivilWar().BuildingModifiers.keys():
		PrefixList.append(CyTranslator().getText("TXT_KEY_BUILDING_DISSENT_MODIFIER", (CivilWar.CivilWar().BuildingModifiers[iBuilding], )))

	# Religious Dissent
	iModifier = 0
	iReligion = BuildingInfo.getReligionType()
	if iReligion > -1:
		if BuildingInfo.getSpecialBuildingType() == gc.getInfoTypeForString('SPECIALBUILDING_GREAT_TEMPLE'):
			iModifier = CivilWar.CivilWar().iGreatTempleDissentModifier
		elif BuildingInfo.getReligionChange(iReligion) > 0:
			iModifier = CivilWar.CivilWar().iShrineDissentModifier

		if iModifier != 0:
			szReligiousDissentModifier = u"%c%d%% Dissent from %c in all Cities" % (CyGame().getSymbolID(FontSymbols.BULLET_CHAR), iModifier, gc.getReligionInfo(iReligion).getChar())
			SuffixList.append(szReligiousDissentModifier)

	# Faith / GPP
	if bCivilopedia:
		if BuildingInfo.getGreatPeopleRateChange() != 0:
			szUnit = gc.getUnitClassInfo(BuildingInfo.getGreatPeopleUnitClass()).getDescription()
			oldString = "City more likely to generate <color=102,229,255,255><link='literal'>" + szUnit + "</link></color>"
			if BuildingInfo.getGreatPeopleUnitClass() == gc.getInfoTypeForString('UNITCLASS_PROPHET'):
				iReligion = BuildingInfo.getPrereqReligion()
				if iReligion > -1:
					newString = u"+%d%c (%c%s)" % (BuildingInfo.getGreatPeopleRateChange(), CyGame().getSymbolID(FontSymbols.RELIGION_CHAR), gc.getReligionInfo(iReligion).getChar(), gc.getReligionInfo(iReligion).getDescription())
				else:
					newString = u"+%d%c (%s)" % (BuildingInfo.getGreatPeopleRateChange(), CyGame().getSymbolID(FontSymbols.RELIGION_CHAR), szUnit)
			else:
				newString  = u"+%d%c (%s)" % (BuildingInfo.getGreatPeopleRateChange(), CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR), szUnit)

			szHelp = szHelp.replace(oldString, newString)

	elif szHelp.find("Great Prophet") > - 1:
		szHelp = szHelp.replace(u"%c (Great Prophet)" % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR), u"%c (Great Prophet)" % CyGame().getSymbolID(FontSymbols.RELIGION_CHAR))

	# Temple Requirements
	iReligion = BuildingInfo.getPrereqReligion()
	if iReligion > -1:
		if BuildingInfo.getType().find("_GREAT_TEMPLE_") > 0:
			nRequired = HR_Religion.NumTemplesRequiredForGreatTemple
			nRequired += (HR_Religion.NumTemplesRequiredForGreatTemple * gc.getWorldInfo(CyMap().getWorldSize()).getBuildingClassPrereqModifier() / 100)
			iTemple = HR_Religion.getReligionTemple(iReligion)
			szRequire = u"Requires %s (%d Total)" % (gc.getBuildingInfo(iTemple).getDescription(), nRequired)
			szRequire = CyTranslator().changeTextColor(szRequire, gc.getInfoTypeForString("COLOR_NEGATIVE_TEXT"))
			SuffixList.append(szRequire)

		elif BuildingInfo.getType().find("_MONASTERY_") > 0:
			nRequired = HR_Religion.NumTemplesRequiredForMonastery
			nRequired += (HR_Religion.NumTemplesRequiredForMonastery * gc.getWorldInfo(CyMap().getWorldSize()).getBuildingClassPrereqModifier() / 100)
			iTemple = HR_Religion.getReligionTemple(iReligion)
			szRequire = u"Requires %s (%d Total)" % (gc.getBuildingInfo(iTemple).getDescription(), nRequired)
			szRequire = CyTranslator().changeTextColor(szRequire, gc.getInfoTypeForString("COLOR_NEGATIVE_TEXT"))
			SuffixList.append(szRequire)

	# Description Prefix
	if len(PrefixList) > 0:
		szPrefix = ""
		szSearch = "Allowed)"
		iPos = szHelp.find(szSearch)
		if iPos > -1:
			iPos += len(szSearch) + 1
		else:
			iPos = szHelp.find(u"%c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR))

		for prefix in PrefixList:
			szPrefix += prefix
			if prefix != PrefixList[-1]:
				szPrefix += "\n"

		if iPos > -1:
			szHelp = szHelp[:iPos] + szPrefix + "\n" + szHelp[iPos:]
		else:
			szHelp = szPrefix + "\n" + szHelp

	# Description Suffix
	if len(SuffixList) > 0:
		szSuffix = ""
		iPos = szHelp.find("<color=255,76,76,255>")
		if iPos == -1:
			szSearch = str(BuildingInfo.getProductionCost()) + u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()
			iPos = szHelp.find(szSearch)

		for suffix in SuffixList:
			szSuffix += suffix
			if suffix != SuffixList[-1]:
				szSuffix += "\n"

		if iPos > -1:
			szHelp = szHelp[:iPos] + szSuffix + "\n" + szHelp[iPos:]
		else:
			szHelp += "\n" + szSuffix

	return szHelp



def getNationalWonderLimit(pCity):
	'Returns the maximum number of National Wonders for this city'
	if CyGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE):
		if gc.getPlayer(pCity.getOwner()).isHuman():
			iLimit = gc.getDefineINT('MAX_NATIONAL_WONDERS_PER_CITY_FOR_OCC')
	else:
		iLimit = gc.getDefineINT('MAX_NATIONAL_WONDERS_PER_CITY')
		if pCity.isCapital():
			iLimit += 1

	return iLimit



def getWorldWonderLimit(pCity):
	'Returns the maximum number of World Wonders for this city (-1 = No Limit)'
	if CyGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE):
		iLimit = -1
	else:
		iLimit = WorldWonderLimits[pCity.getCultureLevel()]

	return iLimit



def getRandomCity(pPlayer):
	''
	CityList = []
	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		CityList.append(loopCity)
		(loopCity, iter) = pPlayer.nextCity(iter, False)

	if CityList != []:
		pCity = CityList[CyGame().getSorenRandNum(len(CityList), "Random City")]
		return pCity

	return None



def listCitiesInRange(iX, iY):
	'Returns a list of all cities within workable distance of a tile'
	lCities = []
	for x in xrange(5):
		for y in xrange(5):
			loopPlot = gc.getMap().plot(iX - 2 + x, iY - 2 + y)
			if not loopPlot.isNone():
				if loopPlot.isCity():
					pCity = loopPlot.getPlotCity()
					if pCity.canWork(loopPlot):
						lCities.append(pCity)
	return lCities



def encodeCity(pCity):
	'Covert city coordinates into a single integer'
	'Useful for passing a city instance via a widget'
	iCityXY = (pCity.getX() * 1000) + pCity.getY()
	return iCityXY



def decodeCity(iCityXY):
	'Convert coded integer into city instance'
	'Useful for passing a city instance via a widget'
	pCity = None
	pPlot = CyMap().plot(iCityXY / 1000, iCityXY % 1000)
	if not pPlot.isNone():
		if pPlot.isCity():
			pCity = pPlot.getPlotCity()

	return pCity