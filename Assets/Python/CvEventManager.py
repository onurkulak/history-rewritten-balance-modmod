from CvPythonExtensions import *
import CvUtil
import CvScreensInterface
import CvDebugTools
import PyHelpers
import Popup as PyPopup
import CvAdvisorUtils
import CvCameraControls
import CvStrategyOverlay
import CvTopCivs
import BugCore

import CvEspionageAdvisor
import CvPlatyBuilderScreen
import WBPlayerScreen
import WBCityEditScreen
import WBUnitScreen
import WBGameDataScreen
import WBPlotScreen

import HR
import HR_Cities
import HR_Map
import HR_Organizations
import HR_Religion
import CivilWar
import StartingPoints
import TechDiffusion
import OOSLogger



### Constants
gc = CyGlobalContext()
MainOpt = BugCore.game.Interface
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo



class CvEventManager:
	def __init__(self):
		#################### ON EVENT MAP ######################
		#print "EVENTMANAGER INIT"

		self.bCtrl = False
		self.bShift = False
		self.bAlt = False
		self.bAllowCheats = False

		# OnEvent Enums
		self.EventLButtonDown = 1
		self.EventLcButtonDblClick = 2
		self.EventRButtonDown = 3
		self.EventBack = 4
		self.EventForward = 5
		self.EventKeyDown = 6
		self.EventKeyUp = 7

		self.__LOG_MOVEMENT = 0
		self.__LOG_BUILDING = 0
		self.__LOG_COMBAT = 0
		self.__LOG_CONTACT = 0
		self.__LOG_IMPROVEMENT =0
		self.__LOG_CITYLOST = 0
		self.__LOG_CITYBUILDING = 0
		self.__LOG_TECH = 0
		self.__LOG_UNITBUILD = 0
		self.__LOG_UNITKILLED = 1
		self.__LOG_UNITLOST = 0
		self.__LOG_UNITPROMOTED = 0
		self.__LOG_UNITSELECTED = 0
		self.__LOG_UNITPILLAGE = 0
		self.__LOG_GOODYRECEIVED = 0
		self.__LOG_GREATPERSON = 0
		self.__LOG_RELIGION = 0
		self.__LOG_RELIGIONSPREAD = 0
		self.__LOG_GOLDENAGE = 0
		self.__LOG_ENDGOLDENAGE = 0
		self.__LOG_WARPEACE = 0
		self.__LOG_PUSH_MISSION = 0



		## EVENTLIST
		self.EventHandlerMap = {
			'mouseEvent'				: self.onMouseEvent,
			'kbdEvent' 					: self.onKbdEvent,
			'ModNetMessage'				: self.onModNetMessage,
			'Init'						: self.onInit,
			'Update'					: self.onUpdate,
			'UnInit'					: self.onUnInit,
			'OnSave'					: self.onSaveGame,
			'OnPreSave'					: self.onPreSave,
			'OnLoad'					: self.onLoadGame,
			'GameStart'					: self.onGameStart,
			'GameEnd'					: self.onGameEnd,
			'plotRevealed' 				: self.onPlotRevealed,
			'plotFeatureRemoved' 		: self.onPlotFeatureRemoved,
			'plotPicked'				: self.onPlotPicked,
			'nukeExplosion'				: self.onNukeExplosion,
			'gotoPlotSet'				: self.onGotoPlotSet,
			'BeginGameTurn'				: self.onBeginGameTurn,
			'EndGameTurn'				: self.onEndGameTurn,
			'BeginPlayerTurn'			: self.onBeginPlayerTurn,
			'EndPlayerTurn'				: self.onEndPlayerTurn,
			'endTurnReady'				: self.onEndTurnReady,
			'combatResult' 				: self.onCombatResult,
		  	'combatLogCalc'	 			: self.onCombatLogCalc,
		  	'combatLogHit'				: self.onCombatLogHit,
			'improvementBuilt' 			: self.onImprovementBuilt,
			'improvementDestroyed' 		: self.onImprovementDestroyed,
			'routeBuilt' 				: self.onRouteBuilt,
			'firstContact' 				: self.onFirstContact,
			'cityBuilt' 				: self.onCityBuilt,
			'cityRazed'					: self.onCityRazed,
			'cityAcquired' 				: self.onCityAcquired,
			'cityAcquiredAndKept' 		: self.onCityAcquiredAndKept,
			'cityLost'					: self.onCityLost,
			'cultureExpansion' 			: self.onCultureExpansion,
			'cityGrowth' 				: self.onCityGrowth,
			'cityDoTurn' 				: self.onCityDoTurn,
			'cityBuildingUnit'			: self.onCityBuildingUnit,
			'cityBuildingBuilding'		: self.onCityBuildingBuilding,
			'cityRename'				: self.onCityRename,
			'cityHurry'					: self.onCityHurry,
			'selectionGroupPushMission'	: self.onSelectionGroupPushMission,
			'unitMove' 					: self.onUnitMove,
			'unitSetXY' 				: self.onUnitSetXY,
			'unitCreated' 				: self.onUnitCreated,
			'unitBuilt' 				: self.onUnitBuilt,
			'unitKilled'				: self.onUnitKilled,
			'unitLost'					: self.onUnitLost,
			'unitPromoted'				: self.onUnitPromoted,
			'unitSelected'				: self.onUnitSelected,
			'UnitRename'				: self.onUnitRename,
			'unitPillage'				: self.onUnitPillage,
			'unitSpreadReligionAttempt'	: self.onUnitSpreadReligionAttempt,
			'unitGifted'				: self.onUnitGifted,
			'unitBuildImprovement'		: self.onUnitBuildImprovement,
			'goodyReceived'        		: self.onGoodyReceived,
			'greatPersonBorn'      		: self.onGreatPersonBorn,
			'buildingBuilt' 			: self.onBuildingBuilt,
			'projectBuilt' 				: self.onProjectBuilt,
			'techAcquired'				: self.onTechAcquired,
			'techSelected'				: self.onTechSelected,
			'religionFounded'			: self.onReligionFounded,
			'religionSpread'			: self.onReligionSpread,
			'religionRemove'			: self.onReligionRemove,
			'corporationFounded'		: self.onCorporationFounded,
			'corporationSpread'			: self.onCorporationSpread,
			'corporationRemove'			: self.onCorporationRemove,
			'goldenAge'					: self.onGoldenAge,
			'endGoldenAge'				: self.onEndGoldenAge,
			'chat' 						: self.onChat,
			'victory'					: self.onVictory,
			'vassalState'				: self.onVassalState,
			'changeWar'					: self.onChangeWar,
			'setPlayerAlive'			: self.onSetPlayerAlive,
			'playerChangeStateReligion'	: self.onPlayerChangeStateReligion,
			'playerGoldTrade'			: self.onPlayerGoldTrade,
			'windowActivation'			: self.onWindowActivation,
			'gameUpdate'				: self.onGameUpdate,		# sample generic event
		}

		################## Events List ###############################
		#
		# Dictionary of Events, indexed by EventID (also used at popup context id)
		#   entries have name, beginFunction, applyFunction [, randomization weight...]
		#
		# Normal events first, random events after
		#
		################## Events List ###############################
		self.Events = {
			CvUtil.EventEditCityName 	 	: ('EditCityName', self.__eventEditCityNameApply, self.__eventEditCityNameBegin),
			CvUtil.EventPlaceObject		 	: ('PlaceObject', self.__eventPlaceObjectApply, self.__eventPlaceObjectBegin),
			CvUtil.EventAwardTechsAndGold	: ('AwardTechsAndGold', self.__eventAwardTechsAndGoldApply, self.__eventAwardTechsAndGoldBegin),

		### Platy World Builder
			CvUtil.EventEditUnitName		: ('EditUnitName', self.__eventEditUnitNameApply, self.__eventEditUnitNameBegin),
			CvUtil.EventWBLandmarkPopup		: ('WBLandmarkPopup', self.__eventWBLandmarkPopupApply, self.__eventWBScriptPopupBegin),

			1111 : ('WBPlayerScript', self.__eventWBPlayerScriptPopupApply, self.__eventWBScriptPopupBegin),
			2222 : ('WBCityScript', self.__eventWBCityScriptPopupApply, self.__eventWBScriptPopupBegin),
			3333 : ('WBUnitScript', self.__eventWBUnitScriptPopupApply, self.__eventWBScriptPopupBegin),
			4444 : ('WBGameScript', self.__eventWBGameScriptPopupApply, self.__eventWBScriptPopupBegin),
			5555 : ('WBPlotScript', self.__eventWBPlotScriptPopupApply, self.__eventWBScriptPopupBegin),
			}



#################### EVENT STARTERS ######################

	def handleEvent(self, argsList):
		'EventMgr entry point'
		# extract the last 6 args in the list, the first arg has already been consumed
		self.origArgsList = argsList	# point to original
		tag = argsList[0]				# event type string
		idx = len(argsList)-6
		bDummy = false
		self.bDbg, bDummy, self.bAlt, self.bCtrl, self.bShift, self.bAllowCheats = argsList[idx:]
		ret = 0
		if self.EventHandlerMap.has_key(tag):
			fxn = self.EventHandlerMap[tag]
			ret = fxn(argsList[1:idx])

		return ret



#################### EVENT APPLY ######################

	def beginEvent( self, context, argsList=-1 ):
		'Begin Event'
		entry = self.Events[context]
		return entry[2]( argsList )



	def applyEvent(self, argsList):
		'Apply the effects of an event'
		context, playerID, netUserData, popupReturn = argsList

		if context == CvUtil.PopupTypeEffectViewer:
			return CvDebugTools.g_CvDebugTools.applyEffectViewer( playerID, netUserData, popupReturn )

		entry = self.Events[context]

		if context not in CvUtil.SilentEvents:
			self.reportEvent(entry, context, (playerID, netUserData, popupReturn) )

		return entry[1](playerID, netUserData, popupReturn)



	def reportEvent(self, entry, context, argsList):
		'Report an Event to Events.log '
		if CyGame().getActivePlayer() != -1:
			message = "DEBUG Event: %s (%s)" %(entry[0], gc.getActivePlayer().getName())
			CyInterface().addImmediateMessage(message, "")
			CvUtil.pyPrint(message)

		return 0



#################### ON EVENTS ######################

	def onKbdEvent(self, argsList):
		'Keypress handler - return 1 if the event was consumed'
		eventType, key, mx, my, px, py = argsList

		if self.bAllowCheats:
			# Notify debug tools of input to allow it to override the control
			argsList = (eventType, key, self.bCtrl, self.bShift, self.bAlt, mx, my, px, py, CyGame().isNetworkMultiPlayer())
			if CvDebugTools.g_CvDebugTools.notifyInput(argsList):
				return 0

		if eventType == self.EventKeyDown:
			# Use 'if' instead of 'elif' or keys will not be detected
			theKey = int(key)
			CvCameraControls.g_CameraControls.handleInput(theKey)

			# AI Auto Play
			if CyGame().getAIAutoPlay():
				if theKey == int(InputTypes.KB_SPACE) or theKey == int(InputTypes.KB_ESCAPE):
					CyGame().setAIAutoPlay(0)
					return 1

			# Tenets Advisor
			if theKey == int(InputTypes.KB_F8) and not self.bShift:
				CvScreensInterface.showTenetsScreen()
				return 1

			# Strategy Overlay
			if theKey == int(InputTypes.KB_X):
				if self.bCtrl:
					CvStrategyOverlay.toggleDotMapEditMode()
					return 1
				elif self.bAlt:
					CvStrategyOverlay.toggleDotMapVisibility()
					return 1

			# Break Endless AI Turn
			if theKey == int(InputTypes.KB_C) and self.bCtrl:
				for iPlayer in xrange(gc.getMAX_PLAYERS()):
					pPlayer = gc.getPlayer(iPlayer)
					if not pPlayer.isNone():
						if pPlayer.isTurnActive():
							CyMessageControl().sendModNetMessage(666, iPlayer, -1, -1, -1)
							return 1

			# Dump OOSLog
			if theKey == int(InputTypes.KB_K) and self.bCtrl:
				CyMessageControl().sendModNetMessage(667, -1, -1, -1, -1)
				return 1

		return 0



	def onModNetMessage(self, argsList):
		'Called whenever CyMessageControl().sendModNetMessage() is called - this is all for you modders!'
		iData1, iData2, iData3, iData4, iData5 = argsList

		# Colonists (iData1 = MessageID, iData2 = PlayerID, iData3 = CityID)
		if iData1 == 700:
			pPlayer = gc.getPlayer(iData2)
			pCity = pPlayer.getCity(iData3)
			for iBuildingClass in HR.Unit.ColonistFreeBuildingClass:
				iBuilding = HR.getPlayerBuilding(pPlayer, iBuildingClass)
				if iBuilding > -1:
					pCity.setNumRealBuilding(iBuilding, 1)
					self.onBuildingBuilt((pCity, iBuilding))

		# Great People Missions (iData1 = MessageID, iData2 = PlayerID, iData3 = UnitID, iData4 = WidgetData2)
		elif iData1 == HR.Mission['MISSION_HUMANITARIAN']:
			pPlayer = gc.getPlayer(iData2)
			pCity = HR.decodeCity(iData4)
			pUnit = pPlayer.getUnit(iData3)
			if pUnit.movesLeft() > 0:
				CivilWar.CivilWar().doHumanitarianMission(iData2, pCity)
				pUnit.NotifyEntity(32)
				pUnit.kill(False, -1)

		elif iData1 == HR.Mission['MISSION_FOUND_RELIGION']:
			pPlayer = gc.getPlayer(iData2)
			pUnit = pPlayer.getUnit(iData3)
			if pUnit.movesLeft() > 0:
				HR_Religion.foundReligion(iData4, pPlayer, pUnit.plot().getPlotCity())
				pUnit.kill(False, -1)

		elif iData1 == HR.Mission['MISSION_REFORMATION']:
			pPlayer = gc.getPlayer(iData2)
			pUnit = pPlayer.getUnit(iData3)
			if pUnit.movesLeft() > 0:
				HR_Religion.Tenets().callReformation(pPlayer, [])
				pUnit.NotifyEntity(32)
				pUnit.kill(False, -1)

		elif iData1 == HR.Mission['MISSION_REFORMATION_RESOLVE']:
			pPlayer = gc.getPlayer(iData2)
			TenetList = []
			TenetDict = {}
			TenetString = str(iData3)

			iCount = 0
			for iTenet in xrange(gc.getNumCivicInfos()):
				if not HR_Religion.Tenets().isTenet(iTenet):
					if pPlayer.isCivic(iTenet):
						TenetList.append(iTenet)
						iCount += 1

				else:
					iCategory = gc.getCivicInfo(iTenet).getCivicOptionType()
					iPosition = iCategory - iCount
					if not (iPosition) in TenetDict.keys():
						TenetDict[iPosition] = []
					TenetDict[iPosition].append(iTenet)

			for i in xrange(len(TenetString)):
				key = i
				index = int(TenetString[i]) - 1
				TenetList.append(TenetDict[key][index])

			bAnarchy = True
			if iData4 == 0:
				bAnarchy = False

			HR_Religion.Tenets().doReformation(pPlayer, TenetList, bAnarchy)

		elif iData1 == HR.Mission['MISSION_REPENTANCE']:
			pPlayer = gc.getPlayer(iData2)
			pUnit = pPlayer.getUnit(iData3)
			if pUnit.movesLeft() > 0:
				HR_Religion.Tenets().doRepentance(pPlayer)
				pUnit.NotifyEntity(32)
				pUnit.kill(False, -1)

		elif iData1 == HR.Mission['MISSION_GREAT_TEMPLE']:
			pPlayer = gc.getPlayer(iData2)
			pUnit = pPlayer.getUnit(iData3)
			pCity =	pUnit.plot().getPlotCity()

			pCity.setNumRealBuilding(iData4, 1)
			self.onBuildingBuilt((pCity, iData4))
			pUnit.kill(False, -1)

		# Inquisition
		elif iData1 == HR.Mission['MISSION_INQUISITION']:
			pPlayer = gc.getPlayer(iData2)
			pUnit = pPlayer.getUnit(iData3)
			if pUnit.movesLeft() > 0:
				HR_Religion.Inquisition().doInquisition(pUnit, iData4, pPlayer)

		# Interface
		elif iData1 == HR.Interface['CHANGE_COMMERCE_PERCENT']:
			CommerceType = [CommerceTypes.COMMERCE_GOLD, CommerceTypes.COMMERCE_RESEARCH, CommerceTypes.COMMERCE_CULTURE, CommerceTypes.COMMERCE_ESPIONAGE]
			gc.getPlayer(iData2).changeCommercePercent(CommerceType[iData3], iData4)
			if iData2 == CyGame().getActivePlayer():
				screen = CvEspionageAdvisor.CvEspionageAdvisor().getScreen()
				if screen.isActive():
					CvEspionageAdvisor.CvEspionageAdvisor().updateEspionageWeights()

		elif iData1 == HR.Interface['CHANGE_SPECIALIST']:
			pCity = HR.decodeCity(iData2)
			pCity.alterSpecialistCount(iData3, iData4)

		elif iData1 == HR.Interface['BUY_SHARE']:
			HR_Organizations.buyShares(iData2, iData3, iData4)

		elif iData1 == HR.Interface['SELL_SHARE']:
			HR_Organizations.sellShares(iData2, iData3, iData4)

		elif iData1 == HR.Interface['CANCEL_TRADE']:
			HR_Organizations.cancelTrade(iData2, iData3)

		# Break Endless AI Turn
		elif iData1 == 666:
			pPlayer = gc.getPlayer(iData2)
			CyInterface().addImmediateMessage("DEBUG: Attempting to break endless AI turn!", "")
			print "### BREAK ENDLESS AI TURN ###"
			print "Active Player: %d (%s)" % (pPlayer.getID(), gc.getCivilizationInfo(pPlayer.getCivilizationType()).getDescription())
			(loopUnit, iter) = pPlayer.firstUnit(False)
			while(loopUnit):
				if loopUnit.movesLeft() > 0 or loopUnit.getGroup().readyToMove(False):
					print "- Unit %d: %s at (%d, %d) Moves = %d, Cargo = %d, Group = %d" % (loopUnit.getID(), loopUnit.getName(), loopUnit.getX(), loopUnit.getY(), loopUnit.movesLeft(), loopUnit.getCargo(), loopUnit.getGroupID())
					loopUnit.finishMoves()
				(loopUnit, iter) = pPlayer.nextUnit(iter, False)
			return 1

		# Dump OOSLog
		elif iData1 == 667:
			OOSLogger.doOOSCheck(True)

		print "Modder's net message!"
		CvUtil.pyPrint('onModNetMessage')



	def onInit(self, argsList):
		'Called when Civ starts up'
		CvUtil.pyPrint('OnInit')



	def onUpdate(self, argsList):
		'Called every frame'
		fDeltaTime = argsList[0]

		# allow camera to be updated
		CvCameraControls.g_CameraControls.onUpdate( fDeltaTime )



	def onWindowActivation(self, argsList):
		'Called when the game window activates or deactivates'
		bActive = argsList[0]



	def onUnInit(self, argsList):
		'Called when Civ shuts down'
		CvUtil.pyPrint('OnUnInit')



	def onPreSave(self, argsList):
		"called before a game is actually saved"
		CvUtil.pyPrint('OnPreSave')



	def onSaveGame(self, argsList):
		"return the string to be saved - Must be a string"
		return ""



	def onLoadGame(self, argsList):
		'Called when a game is loaded'

	### HR Constants
		HR.init()
		OOSLogger.bWroteLog = False

	### Dynamic City Naming
		HR_Cities.init(bDebug = False)
		###

		CvAdvisorUtils.resetNoLiberateCities()
		return 0



	def onGameStart(self, argsList):
		'Called at the start of the game'

	### HR Constants
		HR.init()

	### Starting Points
		MapName = CyMap().getMapScriptName()
		if ".civ" in MapName or ".Civ" in MapName:
			if not CyGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_START):
				if CyGame().getGameTurnYear() == gc.getDefineINT("START_YEAR"):
					MapName = MapName.split(".")[0]
					MapName = MapName.replace("(Mac)", "")
					MapName = MapName.replace("(Windows)", "")
					MapName = MapName.strip()				

					try:
						MapFile = open("Mods/History Rewritten/Assets/XML/Maps/" + MapName + "_StartingPoints.xml")

					except:
						iNameLength = len(MapName)
						iCutPoint = -1
						for iChar in xrange(iNameLength):
							if MapName[iChar] == "\\":
								iCutPoint = iChar

						MapName = MapName[iCutPoint : iNameLength]
						MapFile = open("Mods/History Rewritten/Assets/XML/Maps/" + MapName + "_StartingPoints.xml")

					StartingPoints.readStartingPoints(MapFile)
					MapFile.close()

	### Player Data
		for iPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isAlive():
				HR.doDataChecks(pPlayer, True)

	### Dynamic City Naming
		HR_Cities.init(bDebug = False)

	### Dawn of Man
		if CyGame().getGameTurn() == CyGame().getStartTurn() or CyGame().countNumHumanGameTurnActive() == 0:
			for iPlayer in xrange(gc.getMAX_PLAYERS()):
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer.isAlive() and pPlayer.isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
					popupInfo.setText(u"showDawnOfMan")
					popupInfo.addPopup(iPlayer)
		else:
			CyInterface().setSoundSelectionReady(True)

	## Yield Adjustments
		HR_Map.applyPlotYields(True)
		###

		if gc.getGame().isPbem():
			for iPlayer in xrange(gc.getMAX_PLAYERS()):
				player = gc.getPlayer(iPlayer)
				if (player.isAlive() and player.isHuman()):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_DETAILS)
					popupInfo.setOption1(true)
					popupInfo.addPopup(iPlayer)

		CvAdvisorUtils.resetNoLiberateCities()

		#give free tech to the expansive leaders
		for iPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.hasTrait(HR.Trait.ExtraRoadSpeed):
				iTech = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_FAKE_EXPANSIVE') 
				gc.getTeam(pPlayer.getTeam()).setHasTech(iTech, True, iPlayer, False, False)


	def onGameEnd(self, argsList):
		'Called at the End of the game'
		print("Game is ending")
		return



	def onBeginGameTurn(self, argsList):
		'Called at the beginning of the end of each turn'
		iGameTurn = argsList[0]
		if CyGame().getAIAutoPlay() == 0:
			CvTopCivs.CvTopCivs().turnChecker(iGameTurn)

	### Tech Diffusion
		TechDiffusion.TechDiffusion().doDiffusion()
		###



	def onEndGameTurn(self, argsList):
		'Called at the end of the end of each turn'
		iGameTurn = argsList[0]

	### Organizations
		HR_Organizations.doOrganizations()

	### Olympic Games
		if CyGame().getTurnYear(iGameTurn) >= -800:
			if iGameTurn % 20 == 15:
				OlympicPlayer = []
				for iPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
					pPlayer = gc.getPlayer(iPlayer)
					if pPlayer.isAlive():
						OlympicPlayer.append(pPlayer)

				iPlayerChoice = CyGame().getSorenRandNum(len(OlympicPlayer), "Olympic Games: Player Choice")
				pPlayer = OlympicPlayer[iPlayerChoice]
				iCityChoice = CyGame().getSorenRandNum(pPlayer.getNumCities(), "Olympic Games: City Choice")

				i = 0
				(loopCity, iter) = pPlayer.firstCity(false)
				while(loopCity):
					if i == iCityChoice:
						loopCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_OLYMPIC_GAMES'), 1)
						CyInterface().addMessage(loopCity.getOwner(), True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText('TXT_KEY_MESSAGE_OLYMPIC_GAMES_START', (loopCity.getName(), '')), '', 0, '', ColorTypes(gc.getInfoTypeForString('COLOR_GREEN')), -1, -1, False, False)
						break
					i += 1
					(loopCity, iter) = pPlayer.nextCity(iter, False)

			if iGameTurn % 20 == 0:
				for iPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
					pPlayer = gc.getPlayer(iPlayer)
					if pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_OLYMPIC_GAMES')) > 0:
						pPlayer.removeBuildingClass(gc.getInfoTypeForString('BUILDINGCLASS_OLYMPIC_GAMES'))
						CyInterface().addMessage(iPlayer, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText('TXT_KEY_MESSAGE_OLYMPIC_GAMES_END', ()), '', 0, '', ColorTypes(gc.getInfoTypeForString('COLOR_WHITE')), -1, -1, False, False)
						break
		###



	def onBeginPlayerTurn(self, argsList):
		'Called at the beginning of a players turn'
		iGameTurn, iPlayer = argsList



	def onEndPlayerTurn(self, argsList):
		'Called at the end of a players turn'
		iGameTurn, iPlayer = argsList

		# Civics/Tenets/Faith/Civil War
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive() and not pPlayer.isBarbarian():
			HR.doDataChecks(pPlayer, False)
			HR_Religion.Faith().doFaith(pPlayer)
			CivilWar.CivilWar().checkCivilWar(iPlayer)

			# Anarchy Immunity
			iImmunity = CivilWar.CivilWar().getAnarchyImmunity(pPlayer)
			if iImmunity > 0:
				pPlayer.changeAnarchyTurns(-pPlayer.getAnarchyTurns())
				CivilWar.CivilWar().setAnarchyImmunity(pPlayer, iImmunity - 1)

			# Defy Resolution Anger
			if pPlayer.isCivic(HR_Religion.Tenets().NoDefyResolutionAnger):
				(loopCity, iter) = pPlayer.firstCity(False)
				while(loopCity):
					loopCity.changeDefyResolutionAngerTimer(-loopCity.getDefyResolutionAngerTimer())
					(loopCity, iter) = pPlayer.nextCity(iter, False)

		CvAdvisorUtils.resetAdvisorNags()
		CvAdvisorUtils.endTurnFeats(iPlayer)



	def onEndTurnReady(self, argsList):
		iGameTurn = argsList[0]



	def onFirstContact(self, argsList):
		'Contact'
		iTeamX, iHasMetTeamY = argsList

	## World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return

	### Traits - Improved relations
		if CyGame().isFinalInitialized():
			for iPlayerX in xrange(gc.getMAX_CIV_PLAYERS()):
				pPlayerX = gc.getPlayer(iPlayerX)
				if pPlayerX.isAlive() and pPlayerX.getTeam() == iTeamX:
					if pPlayerX.hasTrait(HR.Trait.AttitudeChange[0]):
						for iPlayerY in xrange(gc.getMAX_CIV_PLAYERS()):
							pPlayerY = gc.getPlayer(iPlayerY)
							if pPlayerY.isAlive() and pPlayerY.getTeam() == iHasMetTeamY:
								pPlayerY.AI_changeAttitudeExtra(iPlayerX, HR.Trait.AttitudeChange[1])

	### Fake Wonders
		pTeam = gc.getTeam(iTeamX)
		if pTeam.isVassal(iHasMetTeamY):
			pPlayer = gc.getPlayer(pTeam.getLeaderID())
			for iTrait, iWonder in HR.Trait.FakeWonder:
				if pPlayer.hasTrait(iTrait):
					capital = pPlayer.getCity(0)
					capital.setNumRealBuilding(iWonder, 1)
		###

		if not self.__LOG_CONTACT:
			return
		CvUtil.pyPrint('Team %d has met Team %d' % (iTeamX, iHasMetTeamY))



	def onCombatResult(self, argsList):
		'Combat Result'
		pWinner, pLoser = argsList
		playerX = PyPlayer(pWinner.getOwner())
		unitX = PyInfo.UnitInfo(pWinner.getUnitType())
		playerY = PyPlayer(pLoser.getOwner())
		unitY = PyInfo.UnitInfo(pLoser.getUnitType())
		iPlayerWin = pWinner.getOwner()
		iPlayerLose = pLoser.getOwner()
		pPlayerWin = gc.getPlayer(iPlayerWin)
		pPlayerLose = gc.getPlayer(iPlayerLose)
		pPlot = CyMap().plot(pLoser.getX(), pLoser.getY())

	### Hunting
		if pLoser.isAnimal():
			if pWinner.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_WARRIOR'):
				# Search for player cities up to 4 tiles away
				CityArray = []
				for x in xrange(9):
					for y in xrange(9):
						loopPlot = gc.getMap().plot(pWinner.getX() - 4 + x, pWinner.getY() - 4 + y)
						if not loopPlot.isNone():
							if loopPlot.isCity():
								pCity = loopPlot.getPlotCity()
								if pCity.getOwner() == iPlayerWin:
									CityArray.append(pCity)

				if len(CityArray) > 0:
					# Minimum food granted is equal to animal strength
					# Maximum food granted is equal to twice animal strength
					iFood = CyGame().getSorenRandNum(pLoser.baseCombatStr() + 1, "Random extra food") + pLoser.baseCombatStr()
					iBuildingClass, iModifier = HR.Building.HuntingModifier
					if pPlayerWin.getBuildingClassCount(iBuildingClass) > 0:
						iFood += (iFood * iModifier / 100)
					iCity = CyGame().getSorenRandNum(len(CityArray), "Choose city for food")
					CityArray[iCity].changeFood(iFood)
					if pPlayerWin.isHuman():
						CyInterface().addMessage(iPlayerWin, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_MESSAGE_FOOD_FROM_ANIMAL", (pWinner.getName(), CityArray[iCity].getName(), iFood)), None, 2, pLoser.getButton(), ColorTypes(13), pLoser.getX(), pLoser.getY(), True, True)

	### Check for Actual Combat
		elif pLoser.getUnitCombatType() > -1:
			if pWinner.getDomainType() == pLoser.getDomainType():

			### Extra Experience
				if pPlayerWin.hasTrait(HR.Trait.ExtraExperience[0]):
					if not pPlayerLose.isBarbarian():
						pWinner.changeExperience(HR.Trait.ExtraExperience[1], -1, True, False, False)

			### Wealth from Combat
				if pPlayerWin.isCivic(HR.Civic.CombatVictoryWealth):
					# Skip defeated barbarians and animals
					if not pPlayerLose.isBarbarian():
						# Is plot within cultural borders?
						if pPlot.getOwner() > -1:
							# Is it rival territory?
							if pPlot.getTeam() != pPlayerWin.getTeam():
								# Defeating units grants wealth
								HR.doCombatCommerce(pPlayerWin, pLoser, pPlot, 0)

			### Faith from Combat
				iTenet, iFaith = HR_Religion.Tenets().HeathenCombatFaith
				if pPlayerWin.isCivic(iTenet):
					if pPlayerLose.getStateReligion() != pPlayerWin.getStateReligion():
						HR_Religion.Faith().changeFaith(pPlayerWin, iFaith)

			### Culture from Combat
			#	if pPlot.getOwner() > -1:
			#		# Skip combat with barbarians
			#		if not pPlayerWin.isBarbarian() and not pPlayerLose.isBarbarian():
			#			# If the winner has the appropriate trait
			#			if pPlayerWin.hasTrait(HR.Trait.CombatVictoryCulture):
			#				# Was combat within the winner's borders?
			#				if pPlot.getOwner() == iPlayerWin:
			#					# Defeating units grants culture
			#					HR.doCombatCommerce(pPlayerWin, pLoser, pPlot, 2)
			#			# If the loser has the appropriate trait
			#			if pPlayerLose.hasTrait(HR.Trait.CombatVictoryCulture):
			#				# Was combat within the loser's borders?
			#				if pPlot.getOwner() == iPlayerLose:
			#					# Defeated units grant culture
			#					HR.doCombatCommerce(pPlayerLose, pLoser, pPlot, 2)

			### Capture/Enslavement
				iUnit = -1
				if pWinner.getUnitType() in HR.Unit.Capture:
					iCaptureChance = CyGame().getSorenRandNum(100, "Capture chance")
					if iCaptureChance < HR.iUnitCaptureChance:
						iUnit = pLoser.getUnitType()

				if pWinner.getUnitType() in HR.Unit.Enslave:
					iEnslaveChance = CyGame().getSorenRandNum(100, "Enslave chance")
					if iEnslaveChance < HR.iUnitEnslaveChance:
						iUnit = gc.getInfoTypeForString('UNIT_WORKER')
					if not CyGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE):
						if iEnslaveChance < (HR.iUnitEnslaveChance / 2):
							iUnit = gc.getInfoTypeForString('UNIT_SETTLER')

				if iUnit > -1:
					newUnit = pPlayerWin.initUnit(iUnit, pWinner.getX(), pWinner.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
					newUnit.finishMoves()
					if newUnit.getUnitType() == pLoser.getUnitType():
						CyInterface().addMessage(iPlayerWin, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CAPTURED", (pWinner.getName(), gc.getUnitInfo(iUnit).getDescription())), '', 0, '', -1, -1, -1, False, False)
					else:
						CyInterface().addMessage(iPlayerWin, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_ENSLAVED", (pWinner.getName(), gc.getUnitInfo(iUnit).getDescription())), '', 0, '', -1, -1, -1, False, False)

			### Incapacitation
				for iStunUnit, iDuration, iLimit in HR.Unit.Incapacitate:
					if pWinner.getUnitType() == iStunUnit:
						count = 0
						pStunPlot = pLoser.plot()
						for iUnit in xrange(pStunPlot.getNumUnits()):
							pUnit = pStunPlot.getUnit(iUnit)
							if not pUnit.isNone():
								if pUnit.getOwner() == iPlayerLose and not pUnit.isDead():
									if not gc.getUnitInfo(pUnit.getUnitType()).isMechUnit():
										if pUnit.getImmobileTimer() == 0:
											pUnit.setImmobileTimer(iDuration)
											count += 1
											if count >= iLimit:
												break

						if count > 0:
							CyInterface().addMessage(iPlayerWin, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_COMBAT_INCAPACITATE", (pWinner.getName(), count, iDuration)), '', 0, '', ColorTypes(gc.getInfoTypeForString('COLOR_WHITE')), -1, -1, False, False)
							sCivAdj = gc.getPlayer(iPlayerLose).getCivilizationAdjective(0)
							CyInterface().addMessage(iPlayerLose, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_COMBAT_INCAPACITATED", (sCivAdj, pWinner.getName(), count, iDuration)), '', 0, '', ColorTypes(gc.getInfoTypeForString('COLOR_RED')), -1, -1, False, False)

		### Fire
			for iFireUnit, iMinDamage, iMaxDamage, iLimit in HR.Unit.Fire:
				if pWinner.getUnitType() == iFireUnit:
					count = 0
					pFirePlot = pLoser.plot()
					for iUnit in xrange(pFirePlot.getNumUnits()):
						pUnit = pFirePlot.getUnit(iUnit)
						if not pUnit.isNone():
							if pUnit.getOwner() == iPlayerLose and not pUnit.isDead():
								if gc.getUnitInfo(pUnit.getUnitType()).getBonusProductionModifier(gc.getInfoTypeForString('BONUS_TIMBER')) > 0:
									iDamage = CyGame().getSorenRandNum(iMaxDamage, "Fire Damage") + iMinDamage
									pUnit.changeDamage(iDamage, False)
									count += 1
									if count >= iLimit:
										break

					if count > 0:
						CyInterface().addMessage(pWinner.getOwner(), True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_COMBAT_FIRE_DAMAGE_DONE", (pUnit.getName(), count)), '', 0, '', ColorTypes(gc.getInfoTypeForString('COLOR_WHITE')), -1, -1, False, False)
						CyInterface().addMessage(pLoser.getOwner(), True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_COMBAT_FIRE_DAMAGE_TAKEN", (count, )), '', 0, '', ColorTypes(gc.getInfoTypeForString('COLOR_RED')), -1, -1, False, False)
				###

		if (not self.__LOG_COMBAT):
			return
		if playerX and playerY and unitX and unitY:
			CvUtil.pyPrint('Player %d Civilization %s Unit %s has defeated Player %d Civilization %s Unit %s'
				%(playerX.getID(), playerX.getCivilizationName(), unitX.getDescription(),
				playerY.getID(), playerY.getCivilizationName(), unitY.getDescription()))



	def onCombatLogCalc(self, argsList):
		'Combat Result'
		genericArgs = argsList[0][0]
		cdAttacker = genericArgs[0]
		cdDefender = genericArgs[1]
		iCombatOdds = genericArgs[2]
		CvUtil.combatMessageBuilder(cdAttacker, cdDefender, iCombatOdds)



	def onCombatLogHit(self, argsList):
		'Combat Message'
		global gCombatMessages, gCombatLog
		genericArgs = argsList[0][0]
		cdAttacker = genericArgs[0]
		cdDefender = genericArgs[1]
		iIsAttacker = genericArgs[2]
		iDamage = genericArgs[3]

		if cdDefender.eOwner == cdDefender.eVisualOwner:
			szDefenderName = gc.getPlayer(cdDefender.eOwner).getNameKey()
		else:
			szDefenderName = CyTranslator().getText("TXT_KEY_TRAIT_PLAYER_UNKNOWN", ())
		if cdAttacker.eOwner == cdAttacker.eVisualOwner:
			szAttackerName = gc.getPlayer(cdAttacker.eOwner).getNameKey()
		else:
			szAttackerName = CyTranslator().getText("TXT_KEY_TRAIT_PLAYER_UNKNOWN", ())

		if (iIsAttacker == 0):
			combatMessage = CyTranslator().getText("TXT_KEY_COMBAT_MESSAGE_HIT", (szDefenderName, cdDefender.sUnitName, iDamage, cdDefender.iCurrHitPoints, cdDefender.iMaxHitPoints))
			CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
			CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
			if (cdDefender.iCurrHitPoints <= 0):
				combatMessage = CyTranslator().getText("TXT_KEY_COMBAT_MESSAGE_DEFEATED", (szAttackerName, cdAttacker.sUnitName, szDefenderName, cdDefender.sUnitName))
				CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
				CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
		elif (iIsAttacker == 1):
			combatMessage = CyTranslator().getText("TXT_KEY_COMBAT_MESSAGE_HIT", (szAttackerName, cdAttacker.sUnitName, iDamage, cdAttacker.iCurrHitPoints, cdAttacker.iMaxHitPoints))
			CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
			CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
			if (cdAttacker.iCurrHitPoints <= 0):
				combatMessage = CyTranslator().getText("TXT_KEY_COMBAT_MESSAGE_DEFEATED", (szDefenderName, cdDefender.sUnitName, szAttackerName, cdAttacker.sUnitName))
				CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
				CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)



	def onImprovementBuilt(self, argsList):
		'Improvement Built'
		iImprovement, iX, iY = argsList
		pPlot = CyMap().plot(iX, iY)

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return

	### Pollution from Improvements
		if CyGame().isFinalInitialized():
			bPolluting = False
			for iPolluter, iMitigationClass in HR.Improvement.Polluting:
				if iImprovement == iPolluter:
					if iMitigationClass == -1:
						bPolluting = True
						HR.addPollution(pPlot)
						break

					else:
						bPolluting = True
						CityArray = HR.listCitiesInRange(iX, iY)
						if len(CityArray) > 0:
							for pCity in CityArray:
								pPlayer = gc.getPlayer(pCity.getOwner())
								iMitigationBuilding = HR.getPlayerBuilding(pPlayer, iMitigationClass)
								if iMitigationBuilding > -1:
									if pCity.getNumBuilding(iMitigationBuilding) > 0:
										bPolluting = False
										break

						if bPolluting:
							if not HR.hasPollution(pPlot):
								bPolluting = True
								HR.addPollution(pPlot)
						break

			if not bPolluting:
				if HR.hasPollution(pPlot):
					HR.removePollution(pPlot)

	### Faster Growth of Cottages
		if gc.getImprovementInfo(iImprovement).getImprovementUpgrade() > -1:
			if pPlot.getOwner() > -1:
				pPlayer = gc.getPlayer(pPlot.getOwner())
				if pPlayer.hasTrait(HR.Trait.ImprovementUpgradeModifier[0]):
					iProgress = pPlot.getUpgradeTimeLeft(iImprovement, pPlot.getOwner()) * (100 + HR.Trait.ImprovementUpgradeModifier[1]) / 100
					pPlot.setUpgradeProgress(iProgress)
		###

		if (not self.__LOG_IMPROVEMENT):
			return
		CvUtil.pyPrint('Improvement %s was built at %d, %d'
			%(PyInfo.ImprovementInfo(iImprovement).getDescription(), iX, iY))



	def onImprovementDestroyed(self, argsList):
		'Improvement Destroyed'
		iImprovement, iOwner, iX, iY = argsList

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return

	### Pollution from Improvements
		if CyGame().isFinalInitialized():
			for iPolluter, iMitigationClass in HR.Improvement.Polluting:
				if iImprovement == iPolluter:
					pPlot = CyMap().plot(iX, iY)
					if HR.hasPollution(pPlot):
						HR.removePollution(pPlot)
		###

		if (not self.__LOG_IMPROVEMENT):
			return
		CvUtil.pyPrint('Improvement %s was Destroyed at %d, %d'
			%(PyInfo.ImprovementInfo(iImprovement).getDescription(), iX, iY))



	def onRouteBuilt(self, argsList):
		'Route Built'
		iRoute, iX, iY = argsList

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return
		###

		if (not self.__LOG_IMPROVEMENT):
			return
		CvUtil.pyPrint('Route %s was built at %d, %d'
			% (gc.getRouteInfo(iRoute).getDescription(), iX, iY))



	def onPlotRevealed(self, argsList):
		'Plot Revealed'
		pPlot = argsList[0]
		iTeam = argsList[1]

	## World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return

	### Natural Wonders
		pTeam = gc.getTeam(iTeam)
		if not pTeam.isBarbarian():
			HR_Map.NaturalWonders().checkNaturalWonderRevealed(pPlot, iTeam)
		###



	def onPlotFeatureRemoved(self, argsList):
		'Plot Feature Removed'
		pPlot = argsList[0]
		pCity = argsList[1]
		iFeatureType = argsList[2]

	### Chopping
		HR.doChopping(pPlot, pCity, False)
		###



	def onPlotPicked(self, argsList):
		'Plot Picked'
		pPlot = argsList[0]
		CvUtil.pyPrint('Plot was picked at %d, %d'
			%(pPlot.getX(), pPlot.getY()))



	def onNukeExplosion(self, argsList):
		'Nuke Explosion'
		pPlot, pNukeUnit = argsList
		CvUtil.pyPrint('Nuke detonated at %d, %d' % (pPlot.getX(), pPlot.getY()))



	def onGotoPlotSet(self, argsList):
		'Nuke Explosion'
		pPlot, iPlayer = argsList



	def onBuildingBuilt(self, argsList):
		'Building Completed - NOT triggered by setNumRealBuilding'
		pCity, iBuildingType = argsList
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		BuildingInfo = gc.getBuildingInfo(iBuildingType)
		iBuildingClass = BuildingInfo.getBuildingClassType()
		BuildingClassInfo = gc.getBuildingClassInfo(iBuildingClass)

		bNationalWonder = isNationalWonderClass(iBuildingClass)
		bWorldWonder = isWorldWonderClass(iBuildingClass)

	### Palace Yield
		if iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_PALACE'):
			for iCivic, YieldType, iYieldChange in HR.Civic.ExtraPalaceYield:
				pCity.setBuildingYieldChange(gc.getInfoTypeForString('BUILDINGCLASS_PALACE'), YieldType, pPlayer.isCivic(iCivic) * iYieldChange)

	### Religious Buildings
		iReligion = BuildingInfo.getReligionType()
		if iReligion > -1 and iReligion == pPlayer.getStateReligion():
			if BuildingInfo.getSpecialBuildingType() == gc.getInfoTypeForString('SPECIALBUILDING_TEMPLE'):

				# Happiness
				iTenet, iHappiness = HR_Religion.Tenets().TempleHappiness
				if pPlayer.isCivic(iTenet):
					pCity.changeExtraHappiness(iHappiness)

				# Health
				iTenet, iHealth = HR_Religion.Tenets().TempleHealth
				if pPlayer.isCivic(iTenet):
					pCity.changeExtraHealth(iHealth)

			elif BuildingInfo.getSpecialBuildingType() == gc.getInfoTypeForString('SPECIALBUILDING_GREAT_TEMPLE'):

				# Specialists
				for iTenet, iSpecialist in HR_Religion.Tenets().GreatTempleSpecialist.items():
					if pPlayer.isCivic(iTenet):
						pCity.changeFreeSpecialistCount(iSpecialist, 1)

				# Golden Age
				iTrait, iModifier = HR.Trait.GreatTempleGoldenAge
				if pPlayer.hasTrait(iTrait):
					iGoldenAgeLength = pPlayer.getGoldenAgeLength() * iModifier / 100
					pPlayer.changeGoldenAgeTurns(iGoldenAgeLength)

			elif BuildingInfo.getSpecialBuildingType() == gc.getInfoTypeForString('SPECIALBUILDING_MONASTERY'):

				# Trade Routes
				iTenet, iTradeRoutes = HR_Religion.Tenets().MonasteryTradeRoutes
				if pPlayer.isCivic(iTenet):
					pCity.changeExtraTradeRoutes(iTradeRoutes)

	### Aqueduct
		elif iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_AQUEDUCT'):
			pPlot = pCity.plot()
			pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_RESERVOIR'), 1)
			# Force existing improvements to accept irrigation
			for i in xrange(21):
				loopPlot = pCity.getCityIndexPlot(i)
				if not loopPlot.isNone():
					if loopPlot.getOwner() == pCity.getOwner():
						iImprovement = loopPlot.getImprovementType()
						if iImprovement > -1:
							if gc.getImprovementInfo(iImprovement).isRequiresIrrigation():
								loopPlot.setImprovementType(-1)
								loopPlot.setImprovementType(iImprovement)

	### Sewer
		elif iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_SEWER'):
			pCity.changePopulation(1)

	### Power Plants
		elif iBuildingType in HR.PowerPriority:
			iPriority = HR.PowerPriority.index(iBuildingType)
			for iPowerPlant in HR.PowerPriority:
				if pCity.getNumBuilding(iPowerPlant) > 0:
					if iPriority > HR.PowerPriority.index(iPowerPlant):
						pCity.setNumRealBuilding(iPowerPlant, 0)
						CyInterface().addMessage(iPlayer, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText('TXT_KEY_MESSAGE_POWER_PLANT_DECOMMISSIONED', (gc.getBuildingInfo(iPowerPlant).getDescription(), pCity.getName())), '', 0, '', gc.getInfoTypeForString('COLOR_WHITE'), -1, -1, False, False)


	### Public Transport
		elif iBuildingClass == gc.getInfoTypeForString('BUILDINGCLASS_PUBLIC_TRANSPORTATION'):
			# Loop through plots surrounding the city
			for i in xrange(21):
				loopPlot = pCity.getCityIndexPlot(i)
				# Check plot exists
				if not loopPlot.isNone():
					if loopPlot.getOwner() == pCity.getOwner():
						# Does the plot have a relevant improvement?
						if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_VILLAGE') or loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TOWN'):
							# Is the plot polluted?
							if HR.hasPollution(loopPlot):
								# Remove pollution from the plot
								HR.removePollution(loopPlot)

	### Wonder: Random Great Person
		elif iBuildingClass == HR.Building.RandomGreatPerson:
			lGreatPeople = ['UNIT_ARTIST', 'UNIT_ENGINEER', 'UNIT_MERCHANT', 'UNIT_PROPHET', 'UNIT_SCIENTIST', 'UNIT_SPY_GREAT']
			iGreatPerson = CyGame().getSorenRandNum(len(lGreatPeople), "Wonder: Random Great Person")
			iUnit = gc.getInfoTypeForString(lGreatPeople[iGreatPerson])
			pCity.createGreatPeople(iUnit, False, False)

	### Wonder: Free Great General
		elif iBuildingClass == HR.Building.FreeGreatGeneral:
			iUnit = gc.getInfoTypeForString('UNIT_GENERAL')
			pCity.createGreatPeople(iUnit, False, False)

	### Wonder: Attitude Change
		iWonderClass, iAttitudeChange = HR.Building.AttitudeChange
		if iBuildingClass == iWonderClass:
			for iRival in xrange(gc.getMAX_CIV_PLAYERS()):
				if iRival != pPlayer.getID():
					pRival = gc.getPlayer(iRival)
					if pRival.isAlive():
						if gc.getTeam(pPlayer.getTeam()).isHasMet(pRival.getTeam()):
							pRival.AI_changeAttitudeExtra(iPlayer, iAttitudeChange)

	### Hotel
		for iWonderYieldClass, iYieldType, iYieldChange in HR.Building.WonderYield:
			if iWonderYieldClass == iBuildingClass:
				iAmount = 0
				for iClass in xrange(gc.getNumBuildingClassInfos()):
					if isWorldWonderClass(iClass):
						iWonder = HR.getPlayerBuilding(pPlayer, iClass)
						if gc.getBuildingInfo(iWonder).getFoundsCorporation() == -1:
							if pCity.getNumActiveBuilding(iWonder) > 0:
								iAmount += iYieldChange

				pCity.setBuildingYieldChange(iWonderYieldClass, iYieldType, iAmount)

			elif bWorldWonder or BuildingInfo.getType().find("_NATURAL_WONDER_") > 0:
				if BuildingInfo.getFoundsCorporation() == -1:
					iWonderYieldBuilding = HR.getPlayerBuilding(pPlayer, iWonderYieldClass)
					if pCity.getNumActiveBuilding(iWonderYieldBuilding) > 0:
						iAmount = pCity.getBuildingYieldChange(iWonderYieldClass, iYieldType) + iYieldChange
						pCity.setBuildingYieldChange(iWonderYieldClass, iYieldType, iAmount)

	### Population Change
		if bNationalWonder or bWorldWonder:
			iTenet, iChange = HR_Religion.Tenets().WonderPopulationChange
			if pPlayer.isCivic(iTenet):
				if pCity.getPopulation() > 1:
					pCity.changePopulation(iChange)
					CyInterface().addMessage(pCity.getOwner(), True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText('TXT_KEY_MESSAGE_WONDER_POPULATION_SACRIFICE', (BuildingInfo.getDescription(), abs(iChange), pCity.getName())), '', 0, '', gc.getInfoTypeForString('COLOR_TEXT_NEGATIVE'), -1, -1, False, False)
		###

		if pCity.getOwner() == CyGame().getActivePlayer() and bWorldWonder:
			if not CyGame().GetWorldBuilderMode():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setData1(iBuildingType)
				popupInfo.setData2(pCity.getID())
				popupInfo.setData3(0)
				popupInfo.setText(u"showWonderMovie")
				popupInfo.addPopup(pCity.getOwner())

		CvAdvisorUtils.buildingBuiltFeats(pCity, iBuildingType)

		if not self.__LOG_BUILDING:
			return
		CvUtil.pyPrint('%s was finished by Player %d Civilization %s' % (BuildingInfo.getDescription(), pCity.getOwner(), pPlayer.getCivilizationDescription(0)))



	def onProjectBuilt(self, argsList):
		'Project Completed'
		pCity, iProjectType = argsList
		game = gc.getGame()
		if pCity.getOwner() == CyGame().getActivePlayer():
			if not CyGame().GetWorldBuilderMode():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setData1(iProjectType)
				popupInfo.setData2(pCity.getID())
				popupInfo.setData3(2)
				popupInfo.setText(u"showWonderMovie")
				popupInfo.addPopup(pCity.getOwner())



	def onSelectionGroupPushMission(self, argsList):
		'selection group mission'
		eOwner = argsList[0]
		eMission = argsList[1]
		iNumUnits = argsList[2]
		listUnitIds = argsList[3]

		if (not self.__LOG_PUSH_MISSION):
			return
		if pHeadUnit:
			CvUtil.pyPrint("Selection Group pushed mission %d" %(eMission))



	def onUnitMove(self, argsList):
		'unit move'
		pPlot, pUnit, pOldPlot = argsList
		player = PyPlayer(pUnit.getOwner())
		unitInfo = PyInfo.UnitInfo(pUnit.getUnitType())
		if (not self.__LOG_MOVEMENT):
			return
		if player and unitInfo:
			CvUtil.pyPrint('Player %d Civilization %s unit %s is moving to %d, %d'
				%(player.getID(), player.getCivilizationName(), unitInfo.getDescription(),
				pUnit.getX(), pUnit.getY()))



	def onUnitSetXY(self, argsList):
		'units xy coords set manually'
		pPlot,pUnit = argsList
		player = PyPlayer(pUnit.getOwner())
		unitInfo = PyInfo.UnitInfo(pUnit.getUnitType())
		if (not self.__LOG_MOVEMENT):
			return



	def onUnitCreated(self, argsList):
		'Unit Completed'
		unit = argsList[0]
		player = PyPlayer(unit.getOwner())

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return
		###

		if not self.__LOG_UNITBUILD:
			return



	def onUnitBuilt(self, argsList):
		'Unit Completed'
		pCity = argsList[0]
		pUnit = argsList[1]
		pPlayer = gc.getPlayer(pUnit.getOwner())

	### Colosseum - Build Rival UUs
		if pCity.getNumActiveBuilding(gc.getInfoTypeForString("BUILDING_COLOSSEUM")) > 0:
			# Is the unit built of a compatible type?
			if pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MELEE") or pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_ARCHER") or pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"):
				iUnitType = pUnit.getUnitType()
				iUnitClass = pUnit.getUnitClassType()
				iDefaultUnit = gc.getUnitClassInfo(iUnitClass).getDefaultUnitIndex()
				if iUnitType == iDefaultUnit:
					lUniqueUnits = []
					# Loop through players
					for iPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
						pRival = gc.getPlayer(iPlayer)
						# Is the rival civilization a valid player?
						if pRival.isAlive():
							# Is the rival civilization part of the city's trade network?
							if pPlayer.canContact(iPlayer) and pPlayer.canTradeNetworkWith(iPlayer):
								iUniqueUnit = gc.getCivilizationInfo(pRival.getCivilizationType()).getCivilizationUnits(iUnitClass)
								# Does this civilization have a unique version of this unit?
								if (iDefaultUnit > -1 and iUniqueUnit > -1 and iDefaultUnit != iUniqueUnit):
									# Allow the UU only if its civilization can also build it
									if pRival.canTrain(iUniqueUnit, False, False):
										# Add the UU to the list of candidates
										lUniqueUnits.append(iUniqueUnit)

					# Continue if the list is not empty
					if len(lUniqueUnits) >= 1:
						# Randomly choose and setup one of the UUs in the list
						chance = CyGame().getSorenRandNum(len(lUniqueUnits), "Colosseum UU")
						iNewUnit = lUniqueUnits[chance]
						iX = pUnit.getX()
						iY = pUnit.getY()
						pNewUnit = pPlayer.initUnit(iNewUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
						# Convert the built unit to the chosen rival UU
						pNewUnit.convert(pUnit)
						pUnit = pNewUnit

	### Monastery Experience
		iStateReligion = pPlayer.getStateReligion()
		if iStateReligion > -1:
			if pUnit.canAcquirePromotionAny():
				iTenet, iExperience = HR_Religion.Tenets().MonasteryExperience
				if pPlayer.isCivic(iTenet):
					iMonastery = HR_Religion.getReligionMonastery(iStateReligion)
					if pCity.getNumBuilding(iMonastery) > 0:
						pUnit.changeExperience(iExperience, -1, False, False, False)

	### Great Temple Promotions
			for iTenet in HR_Religion.Tenets().GreatTemplePromotion.keys():
				if pPlayer.isCivic(iTenet):
					iGreatTemple = HR_Religion.getReligionGreatTemple(iStateReligion)
					if pCity.getNumBuilding(iGreatTemple) > 0:
						iPromotion, UnitCombatList = HR_Religion.Tenets().GreatTemplePromotion[iTenet]
						if (UnitCombatList == [] and pUnit.isPromotionValid(iPromotion)) or pUnit.getUnitCombatType() in UnitCombatList:
							pUnit.setHasPromotion(iPromotion, True)

	### Extra Cargo Space
		if pUnit.cargoSpace() > 0:
			if pPlayer.hasTrait(HR.Trait.ExtraCargoSpace):
				iPromotion = gc.getInfoTypeForString('PROMOTION_CARGO')
				if pUnit.isPromotionValid(iPromotion):
					pUnit.setHasPromotion(iPromotion, True)
		###

		CvAdvisorUtils.unitBuiltFeats(pCity, pUnit)

		if not self.__LOG_UNITBUILD:
			return
		CvUtil.pyPrint('%s was finished by Player %d Civilization %s' % (PyInfo.UnitInfo(pUnit.getUnitType()).getDescription(), pPlayer.getID(), pPlayer.getCivilizationShortDescription(0)))



	def onUnitKilled(self, argsList):
		'Unit Killed'
		unit, iAttacker = argsList
		player = PyPlayer(unit.getOwner())
		attacker = PyPlayer(iAttacker)
		if (not self.__LOG_UNITKILLED):
			return
		CvUtil.pyPrint('Player %d Civilization %s Unit %s was killed by Player %d'
			%(player.getID(), player.getCivilizationName(), PyInfo.UnitInfo(unit.getUnitType()).getDescription(), attacker.getID()))



	def onUnitLost(self, argsList):
		'Unit Lost'
		unit = argsList[0]
		player = PyPlayer(unit.getOwner())

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return
		###

		if (not self.__LOG_UNITLOST):
			return
		CvUtil.pyPrint('%s was lost by Player %d Civilization %s'
			%(PyInfo.UnitInfo(unit.getUnitType()).getDescription(), player.getID(), player.getCivilizationName()))



	def onUnitPromoted(self, argsList):
		'Unit Promoted'
		pUnit, iPromotion = argsList
		player = PyPlayer(pUnit.getOwner())
		if (not self.__LOG_UNITPROMOTED):
			return
		CvUtil.pyPrint('Unit Promotion Event: %s - %s' %(player.getCivilizationName(), pUnit.getName(),))



	def onUnitSelected(self, argsList):
		'Unit Selected'
		unit = argsList[0]
		player = PyPlayer(unit.getOwner())
		if (not self.__LOG_UNITSELECTED):
			return
		CvUtil.pyPrint('%s was selected by Player %d Civilization %s'
			%(PyInfo.UnitInfo(unit.getUnitType()).getDescription(), player.getID(), player.getCivilizationName()))



	def onUnitRename(self, argsList):
		'Unit is renamed'
		pUnit = argsList[0]

		if (pUnit.getOwner() == gc.getGame().getActivePlayer()):
			self.__eventEditUnitNameBegin(pUnit)



	def onUnitPillage(self, argsList):
		'Unit pillages a plot'
		pUnit, iImprovement, iRoute, iOwner = argsList
		iPlotX = pUnit.getX()
		iPlotY = pUnit.getY()
		pPlot = CyMap().plot(iPlotX, iPlotY)

	### Traits - Pillage Immunity
		iPlayer = pPlot.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		if iImprovement > -1:
			if iPlayer > -1 and iPlayer != iOwner:
				if pPlayer.hasTrait(HR.Trait.PillageImmunity):
					pass
					#pPlot.setImprovementType(iImprovement)
					# onImprovementBuilt called automatically

	### Message - Route Destroyed
		if iRoute > -1:
			sUnit = pUnit.getName()
			sRoute = gc.getRouteInfo(iRoute).getDescription()
			iColour = gc.getInfoTypeForString('COLOR_GREEN')
			if iPlayer >- 1:
				if pPlayer.isHuman():
					sAdj = gc.getPlayer(iOwner).getCivilizationAdjective(0)
					if iPlayer != iOwner:
						iColour = gc.getInfoTypeForString('COLOR_RED')
					sText = CyTranslator().getText('TXT_KEY_MISC_YOU_IMP_WAS_DESTROYED', (sRoute, sUnit, sAdj))
					CyInterface().addMessage(pPlot.getOwner(), True, gc.getEVENT_MESSAGE_TIME(), sText, "Assets\\Sounds\\Pillage.wav", 0, "", iColour, pUnit.getX(), pUnit.getY(), False, False)

			if gc.getPlayer(iOwner).isHuman():
				sText = CyTranslator().getText('TXT_KEY_MISC_YOU_UNIT_DESTROYED_IMP', (sUnit, sRoute))
				CyInterface().addMessage(iOwner, True, gc.getEVENT_MESSAGE_TIME(), sText, "Assets\\Sounds\\Pillage.wav", 0, "", iColour, pUnit.getX(), pUnit.getY(), False, False)

		if (not self.__LOG_UNITPILLAGE):
			return
		CvUtil.pyPrint("Player %d's %s pillaged improvement %d and route %d at plot at (%d, %d)"
			%(iOwner, PyInfo.UnitInfo(pUnit.getUnitType()).getDescription(), iImprovement, iRoute, iPlotX, iPlotY))



	def onUnitSpreadReligionAttempt(self, argsList):
		'Unit tries to spread religion to a city'
		pUnit, iReligion, bSuccess = argsList
		iX = pUnit.getX()
		iY = pUnit.getY()
		pPlot = CyMap().plot(iX, iY)
		pCity = pPlot.getPlotCity()

	### Tenets - Successful Missionaries
		if not bSuccess:
			iPlayer = pUnit.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isCivic(HR_Religion.Tenets().MissionarySuccess):
				if pPlayer.getStateReligion() == iReligion:
					pCity.setHasReligion(iReligion, True, True, True)
					CyInterface().addMessage(iPlayer, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText('TXT_KEY_MESSAGE_MISSIONARY_MARTYRDOM', (pUnit.getName(), pCity.getName(), gc.getReligionInfo(iReligion).getDescription())), '', 0, '', -1, -1, -1, False, False)
		###



	def onUnitGifted(self, argsList):
		'Unit is gifted from one player to another'
		pUnit, iGiftingPlayer, pPlotLocation = argsList



	def onUnitBuildImprovement(self, argsList):
		'Unit begins enacting a Build (building an Improvement or Route)'
		pUnit, iBuild, bFinished = argsList



	def onGoodyReceived(self, argsList):
		'Goody received'
		iPlayer, pPlot, pUnit, iGoodyType = argsList

	### Tribal Islands
		if pPlot.isWater():
			if iGoodyType in (gc.getInfoTypeForString("GOODY_WARRIOR"), gc.getInfoTypeForString("GOODY_SETTLER"), gc.getInfoTypeForString("GOODY_SCOUT"), gc.getInfoTypeForString("GOODY_WORKER")):
				iMaxPlotUnit = pPlot.getNumUnits() - 1
				for i in xrange(iMaxPlotUnit, -1, -1):
					pPlotUnit = pPlot.getUnit(i)
					if pPlotUnit.getDomainType() == gc.getInfoTypeForString("DOMAIN_LAND"):
						pPlotUnit.jumpToNearestValidPlot()

			elif iGoodyType in (gc.getInfoTypeForString("GOODY_BARBARIANS_WEAK"), gc.getInfoTypeForString("GOODY_BARBARIANS_STRONG")):
				pBarbarian = gc.getPlayer(gc.getBARBARIAN_PLAYER())
				iPirate = gc.getInfoTypeForString('UNIT_PIRATE')
				iPrivateer = gc.getInfoTypeForString('UNIT_PRIVATEER')

				PlotList = HR_Map.getAdjacentPlots(pPlot, 1, False)
				for adjPlot in PlotList:
					if adjPlot.isUnit() and adjPlot.isWater():
						iMaxPlotUnit = adjPlot.getNumUnits() - 1
						for i in xrange(iMaxPlotUnit, -1, -1):
							adjUnit = adjPlot.getUnit(i)
							if adjUnit.isBarbarian() and adjUnit.getDomainType() == gc.getInfoTypeForString("DOMAIN_LAND"):
								iUnit = -1
								if pBarbarian.canTrain(iPrivateer, False, False):
									iUnit = iPrivateer
								elif pBarbarian.canTrain(iPirate, False, False) or pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_COAST'):
									iUnit = iPirate

								adjUnit.setDamage(100, False)
								if iUnit > -1:
									newUnit = pBarbarian.initUnit(iUnit, adjPlot.getX(), adjPlot.getY(), UnitAITypes.UNITAI_PIRATE_SEA, DirectionTypes.NO_DIRECTION)
		###

		if not self.__LOG_GOODYRECEIVED:
			return
		CvUtil.pyPrint('%s received a goody' % (gc.getPlayer(iPlayer).getCivilizationDescription(0)), )



	def onGreatPersonBorn(self, argsList):
		'Unit Promoted'
		pUnit, iPlayer, pCity = argsList
		pPlayer = gc.getPlayer(iPlayer)

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return

	### Great Prophet
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_PROPHET'):
			if not pPlayer.isHuman():
				HR_Religion.doProphetAI(pPlayer, pCity, pUnit)

			# Religious Buildings
			iStateReligion = pPlayer.getStateReligion()
			if iStateReligion > 0:
				for iTenet in HR_Religion.Tenets().MonasteryCommerce.keys():
					if pPlayer.isCivic(iTenet):
						iMonastery = HR_Religion.getReligionMonastery(iStateReligion)
						iMonasteryClass = gc.getBuildingInfo(iMonastery).getBuildingClassType()
						iCommerceType, iCommerceChange = HR_Religion.Tenets().MonasteryCommerce[iTenet]
						(loopCity, iter) = pPlayer.firstCity(False)
						while(loopCity):
							if loopCity.getNumBuilding(iMonastery) > 0:
								loopCity.setBuildingCommerceChange(iMonasteryClass, iCommerceType, iCommerceChange)
							(loopCity, iter) = pPlayer.nextCity(iter, False)
						break
		###

		if pUnit.isNone() or pCity.isNone():
			return
		if not self.__LOG_GREATPERSON:
			return
		CvUtil.pyPrint('A %s was born for %s in %s' %(pUnit.getName(), pPlayer.getCivilizationDescription(0), pCity.getName()))



	def onTechAcquired(self, argsList):
		'Tech Acquired'
		iTechType, iTeam, iPlayer, bAnnounce = argsList
		# Note that iPlayer may be NULL (-1) and not a refer to a player object

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return
		###

		# Show tech splash when applicable
		if iPlayer > -1 and bAnnounce and not CyInterface().noTechSplash():
			if CyGame().isFinalInitialized() and not CyGame().GetWorldBuilderMode():
				if iPlayer == gc.getGame().getActivePlayer():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
					popupInfo.setData1(iTechType)
					popupInfo.setText(u"showTechSplash")
					popupInfo.addPopup(iPlayer)

		if not self.__LOG_TECH:
			return
		CvUtil.pyPrint('%s was finished by Team %d' % (PyInfo.TechnologyInfo(iTechType).getDescription(), iTeam))



	def onTechSelected(self, argsList):
		'Tech Selected'
		iTechType, iPlayer = argsList
		if not self.__LOG_TECH:
			return
		CvUtil.pyPrint('%s was selected by Player %d' % (PyInfo.TechnologyInfo(iTechType).getDescription(), iPlayer))



	def onReligionFounded(self, argsList):
		'Religion Founded'
		iReligion, iFounder = argsList
		player = PyPlayer(iFounder)

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return
		###

		iCityId = gc.getGame().getHolyCity(iReligion).getID()
		if gc.getGame().isFinalInitialized() and not gc.getGame().GetWorldBuilderMode():
			if iFounder == gc.getGame().getActivePlayer():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setData1(iReligion)
				popupInfo.setData2(iCityId)
				popupInfo.setData3(1)
				popupInfo.setText(u"showWonderMovie")
				popupInfo.addPopup(iFounder)

		if not self.__LOG_RELIGION:
			return
		CvUtil.pyPrint('Player %d Civilization %s has founded %s'
			%(iFounder, player.getCivilizationName(), gc.getReligionInfo(iReligion).getDescription()))



	def onReligionSpread(self, argsList):
		'Religion Has Spread to a City'
		iReligion, iOwner, pCity = argsList
		pPlayer = gc.getPlayer(iOwner)

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return

	### Tenets - Free Temple
		if pPlayer.isCivic(HR_Religion.Tenets().StateReligionSpreadTemple):
			if pPlayer.getStateReligion() == iReligion:
				iTemple = HR_Religion.getReligionTemple(iReligion)
				pCity.setNumRealBuilding(iTemple, 1)
				self.onBuildingBuilt((pCity, iTemple))
		###

		if not self.__LOG_RELIGIONSPREAD:
			return
		CvUtil.pyPrint('%s has spread to Player %d Civilization %s city of %s'
			%(gc.getReligionInfo(iReligion).getDescription(), iOwner, pPlayer.getCivilizationDescription(0), pCity.getName()))



	def onReligionRemove(self, argsList):
		'Religion Has been removed from a City'
		iReligion, iOwner, pRemoveCity = argsList
		player = PyPlayer(iOwner)

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return
		###

		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has been removed from Player %d Civilization %s city of %s'
			%(gc.getReligionInfo(iReligion).getDescription(), iOwner, player.getCivilizationName(), pRemoveCity.getName()))



	def onCorporationFounded(self, argsList):
		'Corporation Founded'
		iCorporation, iFounder = argsList
		pPlayer = gc.getPlayer(iFounder)

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return

	### Corporate Shares
		iShare = HR_Organizations.iFoundingShare
		iTrait, iExtraShare = HR.Trait.CorporationExtraShare
		if pPlayer.hasTrait(iTrait):
			iShare += iExtraShare

		HR_Organizations.initOrganization(iCorporation, 100 - iShare)
		HR_Organizations.setSharePercent(iFounder, iCorporation, iShare)
		###

		if not self.__LOG_RELIGION:
			return
		CvUtil.pyPrint('Player %d Civilization %s has founded %s' % (iFounder, pPlayer.getCivilizationDescription(), gc.getCorporationInfo(iCorporation).getDescription()))



	def onCorporationSpread(self, argsList):
		'Corporation Has Spread to a City'
		iCorporation, iOwner, pSpreadCity = argsList
		player = PyPlayer(iOwner)

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return

	### Corporations
		HR_Organizations.updateCityOrganizations(pSpreadCity)
		###

		if not self.__LOG_RELIGIONSPREAD:
			return
		CvUtil.pyPrint('%s has spread to Player %d Civilization %s city of %s' % (gc.getCorporationInfo(iCorporation).getDescription(), iOwner, player.getCivilizationName(), pSpreadCity.getName()))



	def onCorporationRemove(self, argsList):
		'Corporation has been removed from a City'
		iCorporation, iOwner, pRemoveCity = argsList
		player = PyPlayer(iOwner)

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return
		###

	### Corporations
		HR_Organizations.updateCityOrganizations(pRemoveCity)
		###

		if not self.__LOG_RELIGIONSPREAD:
			return
		CvUtil.pyPrint('%s has been removed from Player %d Civilization %s city of %s' % (gc.getCorporationInfo(iCorporation).getDescription(), iOwner, player.getCivilizationName(), pRemoveCity.getName()))



	def onGoldenAge(self, argsList):
		'Golden Age'
		iPlayer = argsList[0]
		pPlayer = gc.getPlayer(iPlayer)

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return

	### Golden Age Length
		iTenet, iModifier = HR_Religion.Tenets().GoldenAgeLengthModifier
		if pPlayer.isCivic(iTenet):
			iChange = pPlayer.getGoldenAgeLength() * iModifier / 100
			pPlayer.changeGoldenAgeTurns(iChange)

	### Wonder: Shared Religion Golden Ages
		iBuildingClass, iModifier = HR.Building.ReligionSharedGoldenAge
		if CyGame().getBuildingClassCreatedCount(iBuildingClass) > 0:
			if pPlayer.getBuildingClassCount(iBuildingClass) > 0:
				for iRival in xrange(gc.getMAX_CIV_PLAYERS()):
					pRival = gc.getPlayer(iRival)
					if pRival.getBuildingClassCount(iBuildingClass) > 0:
						if pRival.getStateReligion() > -1:
							if pRival.getStateReligion() == pPlayer.getStateReligion():
								iTurns = pRival.getGoldenAgeLength() * iModifier / 100
								pRival.changeGoldenAgeTurns(iTurns)
								break

		if not self.__LOG_GOLDENAGE:
			return
		CvUtil.pyPrint("Player %d Civilization %s has begun a golden age" % (iPlayer, pPlayer.getCivilizationName()))



	def onEndGoldenAge(self, argsList):
		'End Golden Age'
		iPlayer = argsList[0]
		pPlayer = gc.getPlayer(iPlayer)

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return
		###

		if not self.__LOG_ENDGOLDENAGE:
			return
		CvUtil.pyPrint("Player %d Civilization %s golden age has ended" % (iPlayer, pPlayer.getCivilizationName()))



	def onChangeWar(self, argsList):
		'War Status Changes'
		bIsWar = argsList[0]
		iTeam = argsList[1]
		iRivalTeam = argsList[2]

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return
		###

		if not self.__LOG_WARPEACE:
			return
		if bIsWar:
			strStatus = "declared war"
		else:
			strStatus = "declared peace"
		CvUtil.pyPrint('Team %d has %s on Team %d' % (iTeam, strStatus, iRivalTeam))



	def onChat(self, argsList):
		'Chat Message Event'
		chatMessage = "%s" %(argsList[0],)



	def onSetPlayerAlive(self, argsList):
		'Set Player Alive Event'
		iPlayer = argsList[0]
		bNewValue = argsList[1]

	### Dead Culture
		if not bNewValue:
			for i in xrange(CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				iPlotCulture = pPlot.getCulture(iPlayer)
				if iPlotCulture > 0:
					pPlot.changeCulture(gc.getBARBARIAN_PLAYER(), iPlotCulture, True)
					pPlot.setCulture(iPlayer, 0, True)

				pCity = pPlot.getPlotCity()
				if not pCity.isNone():
					iCityCulture = pCity.getCulture(iPlayer)
					if iCityCulture > 0:
						pCity.changeCulture(gc.getBARBARIAN_PLAYER(), iCityCulture, False)
						pCity.setCulture(iPlayer, 0, False)

	### Anarchy Immunity
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive() and not pPlayer.isBarbarian():
			if CyGame().getElapsedGameTurns() > 0:
				HR.doDataChecks(pPlayer, True)
				iTurns = CyGame().goldenAgeLength()
				CivilWar.CivilWar().setAnarchyImmunity(pPlayer, iTurns)
		###

		CvUtil.pyPrint("Player %d's alive status set to: %d" % (iPlayer, int(bNewValue)))



	def onPlayerChangeStateReligion(self, argsList):
		'Player changes his state religion'
		iPlayer, iNewReligion, iOldReligion = argsList

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return

	### Tenets
		pPlayer = gc.getPlayer(iPlayer)
		HR_Religion.adoptReligion(pPlayer, iOldReligion, iNewReligion)
		###



	def onPlayerGoldTrade(self, argsList):
		'Player Trades gold to another player'
		iFromPlayer, iToPlayer, iGoldAmount = argsList



	def onCityBuilt(self, argsList):
		'City Built'
		pCity = argsList[0]
		pPlayer = gc.getPlayer(pCity.getOwner())

	### Dynamic City Naming
		key, name = HR_Cities.selectCity(pCity.getOwner(), pCity.isCapital(), True)
		if name != "":
			pCity.setName(name, True)

	### City Data
		HR.initCityData(pCity, key)

	### Population
		iTrait, iPopulation = HR.Trait.ExtraPopulation
		if pPlayer.hasTrait(iTrait):
			pCity.changePopulation(iPopulation)

	### Culture Level
		for YieldType in HR.Trait.CultureLevelYield.keys():
			iTrait, iYieldChange = HR.Trait.CultureLevelYield[YieldType]
			if pPlayer.hasTrait(iTrait):
				iYield = pCity.getCultureLevel() * iYieldChange
				pCity.changeBaseYieldRate(YieldType, iYield)

	### Extra Palace Yield
		if pCity.isCapital():
			for iCivic, YieldType, iYieldChange in HR.Civic.ExtraPalaceYield:
				pCity.setBuildingYieldChange(gc.getInfoTypeForString('BUILDINGCLASS_PALACE'), YieldType, pPlayer.isCivic(iCivic) * iYieldChange)

	### Spread State Religion
		iStateReligion = pPlayer.getStateReligion()
		if iStateReligion > -1:
			if pPlayer.hasTrait(HR.Trait.SpreadStateReligion):
				pCity.setHasReligion(iStateReligion, True, True, True)

	### Religious Buildings
			iBuildingClass = gc.getBuildingInfo(HR_Religion.getReligionTemple(iStateReligion)).getBuildingClassType()
			for iTenet in HR_Religion.Tenets().TempleYield.keys():
				if pPlayer.isCivic(iTenet):
					iYieldType, iYieldChange = HR_Religion.Tenets().TempleYield[iTenet]
					pCity.setBuildingYieldChange(iBuildingClass, iYieldType, iYieldChange)

	### Trade Routes
		iTrait, iTradeRoutes = HR.Trait.TradeRoutes
		if pPlayer.hasTrait(iTrait):
			pCity.changeExtraTradeRoutes(iTradeRoutes)

	### Free Building Class
		for iTrait in HR.Trait.FreeBuildingClass.keys():
			if pPlayer.hasTrait(iTrait):
				iBuildingClass = HR.Trait.FreeBuildingClass[iTrait]
				iBuilding = HR.getPlayerBuilding(pPlayer, iBuildingClass)
				pCity.setNumRealBuilding(iBuilding, 1)
				self.onBuildingBuilt((pCity, iBuilding))

	### Fake Wonders
		if pCity.isCapital():
			for iCivic, iWonder in HR.Civic.FakeWonder:
				if pPlayer.isCivic(iCivic):
					pCity.setNumRealBuilding(iWonder, 1)

			for iTrait, iWonder in HR.Trait.FakeWonder:
				if pPlayer.hasTrait(iTrait):
					pCity.setNumRealBuilding(iWonder, 1)

	### Colonists - Free Buildings
		iColonistClass = gc.getInfoTypeForString('UNITCLASS_COLONIST')

		if pPlayer.isHuman():
			if pCity.getOwner() == gc.getGame().getActivePlayer():
				if CyInterface().getHeadSelectedUnit() > -1:
					if CyInterface().getHeadSelectedUnit().getUnitClassType() == iColonistClass:
						CyMessageControl().sendModNetMessage(700, pCity.getOwner(), pCity.getID(), -1, -1)
		else:
			iColonist = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(iColonistClass)
			if iColonist > -1:
				iTech = gc.getUnitInfo(iColonist).getPrereqAndTech()
				if gc.getTeam(pPlayer.getTeam()).isHasTech(iTech):
					CyMessageControl().sendModNetMessage(700, pCity.getOwner(), pCity.getID(), -1, -1)

	### Natural Wonders
		HR_Map.NaturalWonders().claimNaturalWonders(pCity, False)
		###



	def onCityRazed(self, argsList):
		'City Razed'
		pCity, iPlayer = argsList
		iOwner = pCity.findHighestCulture()
		pPlayer = gc.getPlayer(iPlayer)
		pPlot = pCity.plot()
		sConqueror = pPlayer.getName()

	### Aqueduct
		if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_RESERVOIR'):
			if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_DESERT') and pPlot.isRiver():
				pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_FLOODPLAIN'), -1)
			else:
				pPlot.setFeatureType(-1, 1)

	### Corporations - Destroyed HQs
		#if pCity.isHeadquarters():
			# Option 1: automatically relocate Headquarters
			# Option 2: treat corporation as foreign for all players
			# Option 3: treat corporation as domestic for all players

	### Natural Wonders
		HR_Map.NaturalWonders().claimNaturalWonders(pCity, True)
		###

	### Messages - Wonder Destroyed
		if pCity.getNumWorldWonders() > 0:
			# Loop through all possible buildings
			for i in xrange(gc.getNumBuildingInfos()):
				# Did this building exist in the city?
				if pCity.getNumBuilding(i) > 0:
					nBuilding = gc.getBuildingInfo(i)
					# Was the building a world wonder?
					if isWorldWonderClass(nBuilding.getBuildingClassType()):
						sWonder = nBuilding.getDescription()
						# Loop through all players
						for iPlayerX in xrange (gc.getMAX_CIV_PLAYERS()):
							# Is the player the conqueror?
							if iPlayerX == iPlayer:
								CyInterface().addMessage(iPlayerX, False, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_MESSAGE_WONDER_DESTROYED_BY_PLAYER", (sConqueror, sWonder)), "", 0, nBuilding.getButton(), ColorTypes(gc.getInfoTypeForString("COLOR_RED")), pCity.getX(), pCity.getY(), True, True)
							# Or has the player met the conqueror?
							elif gc.getTeam(gc.getPlayer(iPlayerX).getTeam()).isHasMet(pPlayer.getTeam()):
								CyInterface().addMessage(iPlayerX, False, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_MESSAGE_WONDER_DESTROYED", (sConqueror, sWonder)), "", 0, nBuilding.getButton(), ColorTypes(gc.getInfoTypeForString("COLOR_RED")), pCity.getX(), pCity.getY(), True, True)

		# Partisans!
		if pCity.getPopulation > 1 and iOwner != -1 and iPlayer != -1:
			owner = gc.getPlayer(iOwner)
			if not owner.isBarbarian() and owner.getNumCities() > 0:
				if gc.getTeam(owner.getTeam()).isAtWar(gc.getPlayer(iPlayer).getTeam()):
					if gc.getNumEventTriggerInfos() > 0: # prevents mods that don't have events from getting an error
						iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_PARTISANS')
						if iEvent != -1 and gc.getGame().isEventActive(iEvent) and owner.getEventTriggerWeight(iEvent) < 0:
							triggerData = owner.initTriggeredData(iEvent, true, -1, pCity.getX(), pCity.getY(), iPlayer, pCity.getID(), -1, -1, -1, -1)

		CvUtil.pyPrint("City Razed Event: %s" %(pCity.getName(),))



	def onCityAcquired(self, argsList):
		'City Acquired'
		iPreviousOwner, iNewOwner, pCity, bConquest, bTrade = argsList
		pNewOwner = gc.getPlayer(iNewOwner)
		pOldOwner = gc.getPlayer(iPreviousOwner)
		iOwner = pCity.findHighestCulture()
		iX = pCity.getX()
		iY = pCity.getY()
		iCity = pCity.getID()

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return

	### Dynamic City Naming
		if not bConquest: # Conquered cities are handled in onCityAcquiredAndKept
			HR_Cities.renameCity(pCity, iPreviousOwner, iNewOwner)

	### Resistance
		if bConquest:
			iModifier = (CyGame().getGameSpeedType() + 1) * 50
			iResistance = max(2 ,(pCity.getOccupationTimer() * iModifier) / 100)
			if pNewOwner.hasTrait(HR.Trait.NoResistance):
				iResistance = 0
			pCity.setOccupationTimer(iResistance)

	### Improved Plunder
		if bConquest:
			iCivic = HR.Civic.ImprovedPlunder
			iTrait = HR.Trait.ImprovedPlunder

			if pNewOwner.hasTrait(iTrait) or pNewOwner.isCivic(iCivic):
				iCaptureGold = 0
				iCaptureGold += gc.getDefineINT("BASE_CAPTURE_GOLD")
				iCaptureGold += (pCity.getPopulation() * gc.getDefineINT("CAPTURE_GOLD_PER_POPULATION"))
				iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND1"), "Capture Gold 1")
				iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND2"), "Capture Gold 2")
				if (gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS") > 0):
					iCaptureGold *= cyIntRange((CyGame().getGameTurn() - pCity.getGameTurnFounded()), 0, gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS"))
					iCaptureGold /= gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS")

				if pNewOwner.isCivic(iCivic) and pNewOwner.hasTrait(iTrait):
					iCaptureGold *= 2

				if iCaptureGold > 0:
					pNewOwner.changeGold(iCaptureGold)
					pOldOwner.changeGold(-iCaptureGold)
					CyInterface().addMessage(iNewOwner, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_MESSAGE_EXTRA_PLUNDER",(iCaptureGold, pCity.getName())), None, 2, None, ColorTypes(gc.getInfoTypeForString('COLOR_GREEN')), 0, 0, False, False)

	# Partisans!
		if pCity.getPopulation > 1 and iOwner != -1 and iOwner == iPreviousOwner and iNewOwner != -1:
			owner = gc.getPlayer(iOwner)
			iTrait = HR.Trait.PillageImmunity

			if not owner.isBarbarian() and owner.getNumCities() > 0 and owner.hasTrait(iTrait):
				if gc.getTeam(owner.getTeam()).isAtWar(gc.getPlayer(iNewOwner).getTeam()):
					if gc.getNumEventTriggerInfos() > 0: # prevents mods that don't have events from getting an error
						iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_PARTISANS')
						if iEvent != -1 and gc.getGame().isEventActive(iEvent):
							triggerData = owner.initTriggeredData(iEvent, true, -1, pCity.getX(), pCity.getY(), iNewOwner, pCity.getID(), -1, -1, -1, -1)

	### Capture Research
		if pNewOwner.hasTrait(HR.Trait.CaptureResearch):
			iOldTeam = pOldOwner.getTeam()
			iNewTeam = pNewOwner.getTeam()
			pOldTeam = gc.getTeam(iOldTeam)
			pNewTeam = gc.getTeam(iNewTeam)

			if pCity.calculateTeamCulturePercent(iNewTeam) < 25:
				# Choose Techs
				lTechs = []
				for iTech in xrange(gc.getNumTechInfos()):
					if pNewTeam.isHasTech(iTech):
						continue
					if not pNewOwner.canResearch(iTech, False):
						continue
					if pOldTeam.isHasTech(iTech):
						lTechs.append(iTech)

				if len(lTechs) > 0:
					iConquestTech = lTechs[CyGame().getSorenRandNum(len(lTechs), "Choose Conquest Tech")]
					iCost = pNewTeam.getResearchCost(iConquestTech)
					iConquestAmount = pCity.getPopulation() * iCost / 10	# 10% of Tech Cost per Population
					iProgress = pNewTeam.getResearchProgress(iConquestTech)
					pNewTeam.changeResearchProgress(iConquestTech, min(iCost - iProgress, iConquestAmount), iNewOwner)

					# Display Message
					sTech = gc.getTechInfo(iConquestTech).getDescription()
					for iPlayerX in xrange(gc.getMAX_CIV_PLAYERS()):
						pPlayerX = gc.getPlayer(iPlayerX)
						if pPlayerX.isAlive() and pPlayerX.getTeam() == iNewTeam:
							if iConquestAmount < iCost - iProgress:
								CyInterface().addMessage(iPlayerX, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_MESSAGE_CAPTURE_PARTIAL_TECH",(iConquestAmount, sTech, pCity.getName(),)), '', 0, gc.getTechInfo(iConquestTech).getButton(), gc.getInfoTypeForString('COLOR_GREEN'), pCity.getX(), pCity.getY(), True, True)

							else:
								CyInterface().addMessage(iPlayerX, True, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_MESSAGE_CAPTURE_TECH",(sTech, pCity.getName(), )), '', 0, gc.getTechInfo(iConquestTech).getButton(), gc.getInfoTypeForString('COLOR_GREEN'), pCity.getX(), pCity.getY(), True, True)

	### Extra Palace Yield
		pCapital = pOldOwner.getCapitalCity()
		for iCivic, YieldType, iYieldChange in HR.Civic.ExtraPalaceYield:
			pCapital.setBuildingYieldChange(gc.getInfoTypeForString('BUILDINGCLASS_PALACE'), YieldType, pOldOwner.isCivic(iCivic) * iYieldChange)

	### Trade Routes
		iTrait, iTradeRoutes = HR.Trait.TradeRoutes
		if pNewOwner.hasTrait(iTrait):
			pCity.changeExtraTradeRoutes(iTradeRoutes)

	### Free Specialists
		for iBuilding in xrange(gc.getNumBuildingInfos()):
			BuildingInfo = gc.getBuildingInfo(iBuilding)
			if BuildingInfo.getType().startswith("BUILDING_NATURAL_WONDER_"):
				if pCity.getNumBuilding(iBuilding) > 0:
					for iTenet, iSpecialist in HR_Religion.Tenets().NaturalWonderSpecialists.items():
						if pOldOwner.isCivic(iTenet):
							pCity.changeFreeSpecialistCount(iSpecialist, -1)
						if pNewOwner.isCivic(iTenet):
							pCity.changeFreeSpecialistCount(iSpecialist, 1)

	### Free Building Class
		for iTrait in HR.Trait.FreeBuildingClass.keys():
			if pNewOwner.hasTrait(iTrait):
				iBuildingClass = HR.Trait.FreeBuildingClass[iTrait]
				iBuilding = HR.getPlayerBuilding(pNewOwner, iBuildingClass)
				pCity.setNumRealBuilding(iBuilding, 1)
				self.onBuildingBuilt((pCity, iBuilding))

	### Fake Wonders
		for iCivic, iWonder in HR.Civic.FakeWonder:
			if pCity.getNumBuilding(iWonder) > 0:
				pCity.setNumRealBuilding(iWonder, 0)
				pOldOwner.getCapitalCity().setNumRealBuilding(iWonder, 1)

		for iTrait, iWonder in HR.Trait.FakeWonder:
			if pCity.getNumBuilding(iWonder) > 0:
				pCity.setNumRealBuilding(iWonder, 0)
				pOldOwner.getCapitalCity().setNumRealBuilding(iWonder, 1)

	### Religious Buildings
		iOldStateReligion = pOldOwner.getStateReligion()
		iNewStateReligion = pNewOwner.getStateReligion()
		for iTenet in HR_Religion.Tenets().TempleYield.keys():
			iYieldType, iYieldChange = HR_Religion.Tenets().TempleYield[iTenet]

			if iOldStateReligion > -1:
				if pOldOwner.isCivic(iTenet):
					iBuildingClass = gc.getBuildingInfo(HR_Religion.getReligionTemple(iOldStateReligion)).getBuildingClassType()
					pCity.setBuildingYieldChange(iBuildingClass, iYieldType, 0)

			if iNewStateReligion > -1:
				if pNewOwner.isCivic(iTenet):
					iBuildingClass = gc.getBuildingInfo(HR_Religion.getReligionTemple(iNewStateReligion)).getBuildingClassType()
					pCity.setBuildingYieldChange(iBuildingClass, iYieldType, iYieldChange)

		iTenet, iTradeRoutes = HR_Religion.Tenets().MonasteryTradeRoutes
		if pNewOwner.isCivic(iTenet) and iNewStateReligion > -1:
			if pCity.getNumBuilding(HR_Religion.getReligionMonastery(iNewStateReligion)) > 0:
				pCity.changeExtraTradeRoutes(iTradeRoutes)

		for iReligion in xrange(gc.getNumReligionInfos()):
			iMonasteryClass = gc.getBuildingInfo(HR_Religion.getReligionMonastery(iReligion)).getBuildingClassType()
			for iCommerceType in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
				iCommerceChange = -1 * pCity.getBuildingCommerceChange(iMonasteryClass, iCommerceType)
				pCity.setBuildingCommerceChange(iMonasteryClass, iCommerceType, iCommerceChange)

	### Aqueduct
		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_AQUEDUCT')) > 0:
			pPlot = CyMap().plot(iX, iY)
			pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_RESERVOIR'), 1)

	### Hotel
		for iWonderYieldClass, iYieldType, iYieldChange in HR.Building.WonderYield:
			iWonderYieldBuilding = HR.getPlayerBuilding(pNewOwner, iWonderYieldClass)
			if pCity.getNumActiveBuilding(iWonderYieldBuilding) > 0:
				iAmount = 0
				for iClass in xrange(gc.getNumBuildingClassInfos()):
					ClassInfo = gc.getBuildingClassInfo(iClass)
					if isWorldWonderClass(iClass) or ClassInfo.getType().find("NATURAL_WONDER"):
						iWonder = HR.getPlayerBuilding(pNewOwner, iClass)
						if gc.getBuildingInfo(iWonder).getFoundsCorporation() == -1:
							if pCity.getNumActiveBuilding(iWonder) > 0:
								iAmount += iYieldChange

				pCity.setBuildingYieldChange(iWonderYieldClass, iYieldType, iAmount)

	### Hagia Sophia - Capturing UBs
		if pNewOwner.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_HAGIA_SOPHIA')) > 0:
			if not pOldOwner.isBarbarian():
				civ_type = pOldOwner.getCivilizationType()
				# Loop through all classes of buildings
				for iBuildingClass in xrange(gc.getNumBuildingClassInfos()):
					iUniqueBuilding = gc.getCivilizationInfo(pOldOwner.getCivilizationType()).getCivilizationBuildings(iBuildingClass)
					iUniqueBuilding2 = gc.getCivilizationInfo(pNewOwner.getCivilizationType()).getCivilizationBuildings(iBuildingClass)
					iDefaultBuilding = gc.getBuildingClassInfo(iBuildingClass).getDefaultBuildingIndex()
					# Is this building a unique building?
					if iDefaultBuilding > -1 and iDefaultBuilding != iUniqueBuilding and iDefaultBuilding == iUniqueBuilding2: # Do not replace your own UB...
						# Does the captured city still have such a building?
						# If not destroyed when the city fell it will have reverted to the non-unique version
						if pCity.getNumActiveBuilding(iDefaultBuilding):
							# Remove the captured non-unique building
							pCity.setNumRealBuilding(iDefaultBuilding, 0)
							# Replace it with the unique building
							pCity.setNumRealBuilding(iUniqueBuilding, 1)
							self.onBuildingBuilt((pCity, iUniqueBuilding))
							# Message notifying of UB capture
							CyInterface().addMessage(iNewOwner, False, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_BUILDING_HAGIA_SOPHIA_MESSAGE", (pCity.getName(), gc.getBuildingInfo(iUniqueBuilding).getDescription(), gc.getBuildingInfo(iDefaultBuilding).getDescription())), '', 0, gc.getBuildingInfo(iUniqueBuilding).getButton(), ColorTypes(11), pCity.getX(), pCity.getY(), True, True)

		###

		CvUtil.pyPrint('City Acquired Event: %s' % pCity.getName())



	def onCityAcquiredAndKept(self, argsList):
		'Called when city conquered and not razed'
		'Not called when city traded or liberated'
		iOwner, pCity = argsList
		pNewOwner = gc.getPlayer(pCity.getOwner())
		sConqueror = pNewOwner.getName()

	### Dynamic City Naming
		HR_Cities.renameCity(pCity, pCity.getPreviousOwner(), pCity.getOwner())

	### Message - Wonder Captured
		if pCity.getNumWorldWonders() > 0:
			# Loop through all possible buildings
			for i in xrange(gc.getNumBuildingInfos()):
				# Does the building exist in the city?
				if pCity.getNumBuilding(i) > 0:
					nBuilding = gc.getBuildingInfo(i)
					# Is the building a world wonder?
					if isWorldWonderClass(nBuilding.getBuildingClassType()):
						sWonder = nBuilding.getDescription()
						# Loop through all players
						for iPlayer in xrange (gc.getMAX_CIV_PLAYERS()):
							pPlayer = gc.getPlayer(iPlayer)
							if pPlayer.isAlive() and pPlayer.isHuman():
								# Is the player the conqueror?
								if iPlayer == pCity.getOwner():
									CyInterface().addMessage(iPlayer, False, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_MESSAGE_WONDER_CAPTURED_BY_PLAYER", (sConqueror, sWonder)), "", 0, nBuilding.getButton(), ColorTypes(gc.getInfoTypeForString('COLOR_GREEN')), pCity.getX(), pCity.getY(), True, True)
								# Or has the player met the conqueror?
								elif gc.getTeam(pPlayer.getTeam()).isHasMet(pNewOwner.getTeam()):
									CyInterface().addMessage(iPlayer, False, gc.getEVENT_MESSAGE_TIME(), CyTranslator().getText("TXT_KEY_MESSAGE_WONDER_CAPTURED", (sConqueror, sWonder)), "", 0, nBuilding.getButton(), ColorTypes(gc.getInfoTypeForString('COLOR_RED')), pCity.getX(), pCity.getY(), True, True)
		###

		CvUtil.pyPrint('City Acquired and Kept Event: %s' %(pCity.getName()))



	def onCityLost(self, argsList):
		'City Lost'
		city = argsList[0]
		player = PyPlayer(city.getOwner())
		if not self.__LOG_CITYLOST:
			return
		CvUtil.pyPrint('City %s was lost by Player %d Civilization %s' % (city.getName(), player.getID(), player.getCivilizationName()))



	def onCultureExpansion(self, argsList):
		'City Culture Expansion'
		pCity = argsList[0]
		iPlayer = argsList[1]
		pPlayer = gc.getPlayer(iPlayer)

	### World Builder
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
			return
		###
		CvUtil.pyPrint("City %s's culture has expanded" % (pCity.getName(), ))



	def onCityGrowth(self, argsList):
		'City Population Growth'
		pCity = argsList[0]
		iPlayer = argsList[1]

	### Food Storage
		pPlayer = gc.getPlayer(iPlayer)
		iTenet, iModifier = HR_Religion.Tenets().FoodStoredModifier
		if pPlayer.isCivic(iTenet):
			iChange = pCity.getFood() * iModifier / 100
			pCity.setFood(pCity.getFood() + iChange)
		###

		CvUtil.pyPrint("%s has grown" % (pCity.getName(), ))



	def onCityDoTurn(self, argsList):
		'City Production'
		pCity = argsList[0]
		iPlayer = argsList[1]
		pPlayer = gc.getPlayer(iPlayer)

	### Avoid Growth
		if iPlayer == CyGame().getActivePlayer():
			if MainOpt.isAutoAvoidGrowth():
				if pCity.getFoodTurnsLeft() < 2 and (pCity.happyLevel() <= pCity.unhappyLevel(0) or pCity.goodHealth() <= pCity.badHealth(False)):
					pCity.doTask(TaskTypes.TASK_SET_EMPHASIZE, gc.getInfoTypeForString("EMPHASIZE_AVOID_GROWTH"), -1, True)

			if MainOpt.isAutoResumeGrowth():
				if pCity.getFoodTurnsLeft() > 1 or (pCity.happyLevel() > pCity.unhappyLevel(0) and pCity.goodHealth() > pCity.badHealth(False)):
					pCity.doTask(TaskTypes.TASK_SET_EMPHASIZE, gc.getInfoTypeForString("EMPHASIZE_AVOID_GROWTH"), -1, False)

	### Culture Level Yields
		iNewLevel = pCity.getCultureLevel()
		iOldLevel = HR.getCityCulture(pCity)
		if iNewLevel != iOldLevel:
			if pCity.isOccupation():
				HR.setCityCulture(pCity, 0)

			else:
				HR.setCityCulture(pCity, iNewLevel)
				for YieldType in HR.Trait.CultureLevelYield.keys():
					iTrait, iYieldChange = HR.Trait.CultureLevelYield[YieldType]
					if pPlayer.hasTrait(iTrait):
						iChange = iYieldChange * (iNewLevel - iOldLevel)
						pCity.changeBaseYieldRate(YieldType, iChange)

	### Climate Change
		HR_Map.ClimateChange().doClimateChange(pCity)

	### Pyramids
		if not pCity.isDisorder():
			if pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_PYRAMID')) > 0:
				if pCity.getProductionUnit() == gc.getInfoTypeForString('UNIT_WORKER') or pCity.getProductionUnit() == gc.getInfoTypeForString('UNIT_LABOURER'):
					pCity.changeFood(pCity.getYieldRate(0) - pCity.foodConsumption(False, 0))
					if pCity.getFood() > pCity.growthThreshold():
						if pCity.AI_isEmphasize(gc.getInfoTypeForString('EMPHASIZE_AVOID_GROWTH')):
							pCity.setFood(pCity.growthThreshold())
						else:
							pCity.setFood(pCity.getFood() - pCity.growthThreshold() + pCity.getFoodKept())
							pCity.changePopulation(1)
		###
		CvAdvisorUtils.cityAdvise(pCity, iPlayer)



	def onCityBuildingUnit(self, argsList):
		'City begins building a unit'
		pCity = argsList[0]
		iUnitType = argsList[1]
		if not self.__LOG_CITYBUILDING:
			return
		CvUtil.pyPrint("%s has begun building a %s" %(pCity.getName(),gc.getUnitInfo(iUnitType).getDescription()))



	def onCityBuildingBuilding(self, argsList):
		'City begins building a Building'
		pCity = argsList[0]
		iBuildingType = argsList[1]
		if not self.__LOG_CITYBUILDING:
			return
		CvUtil.pyPrint("%s has begun building a %s" %(pCity.getName(),gc.getBuildingInfo(iBuildingType).getDescription()))



	def onCityRename(self, argsList):
		'City is renamed'
		pCity = argsList[0]
		if pCity.getOwner() == gc.getGame().getActivePlayer():
			self.__eventEditCityNameBegin(pCity, True)



	def onCityHurry(self, argsList):
		'City is renamed'
		pCity = argsList[0]
		iHurryType = argsList[1]



	def onVictory(self, argsList):
		'Victory'
		iTeam, iVictory = argsList
		if iVictory >= 0 and iVictory < gc.getNumVictoryInfos():
			victoryInfo = gc.getVictoryInfo(int(iVictory))
			CvUtil.pyPrint("Victory!  Team %d achieves a %s victory"
				%(iTeam, victoryInfo.getDescription()))



	def onVassalState(self, argsList):
		'Vassal State'
		iMaster, iVassal, bVassal = argsList

		if bVassal:
			CvUtil.pyPrint("Team %d becomes a Vassal State of Team %d"
				%(iVassal, iMaster))
		else:
			CvUtil.pyPrint("Team %d revolts and is no longer a Vassal State of Team %d"
				%(iVassal, iMaster))



	def onGameUpdate(self, argsList):
		'sample generic event, called on each game turn slice'
		genericArgs = argsList[0][0]
		turnSlice = genericArgs[0]
		OOSLogger.doOOSCheck(False)



	def onMouseEvent(self, argsList):
		'mouse handler - returns 1 if the event was consumed'
		eventType, mx, my, px, py, interfaceConsumed, screens = argsList
		if px != -1 and py != -1:
			if eventType == self.EventLButtonDown:
				if self.bAllowCheats and self.bCtrl and self.bAlt and CyMap().plot(px,py).isCity() and not interfaceConsumed:
					# Launch Edit City Event
					self.beginEvent(CvUtil.EventEditCity, (px,py))
					return 1

				elif self.bAllowCheats and self.bCtrl and self.bShift and not interfaceConsumed:
					# Launch Place Object Event
					self.beginEvent(CvUtil.EventPlaceObject, (px, py))
					return 1

		if eventType == self.EventBack:
			return CvScreensInterface.handleBack(screens)
		elif eventType == self.EventForward:
			return CvScreensInterface.handleForward(screens)

		return 0



#################### TRIGGERED EVENTS ##################

	def __eventPlaceObjectBegin(self, argsList):
		'Place Object Event'
		CvDebugTools.CvDebugTools().initUnitPicker(argsList)



	def __eventPlaceObjectApply(self, playerID, userData, popupReturn):
		'Place Object Event Apply'
		if (getChtLvl() > 0):
			CvDebugTools.CvDebugTools().applyUnitPicker( (popupReturn, userData) )



	def __eventAwardTechsAndGoldBegin(self, argsList):
		'Award Techs & Gold Event'
		CvDebugTools.CvDebugTools().cheatTechs()



	def __eventAwardTechsAndGoldApply(self, playerID, netUserData, popupReturn):
		'Award Techs & Gold Event Apply'
		if (getChtLvl() > 0):
			CvDebugTools.CvDebugTools().applyTechCheat( (popupReturn) )



	def __eventShowWonderBegin(self, argsList):
		'Show Wonder Event'
		CvDebugTools.CvDebugTools().wonderMovie()



	def __eventShowWonderApply(self, playerID, netUserData, popupReturn):
		'Wonder Movie Apply'
		if (getChtLvl() > 0):
			CvDebugTools.CvDebugTools().applyWonderMovie( (popupReturn) )



	def __eventEditCityNameBegin(self, city, bRename):
		popup = PyPopup.PyPopup(CvUtil.EventEditCityName, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setUserData((city.getID(), bRename, CyGame().getActivePlayer()))
		popup.setHeaderString(CyTranslator().getText("TXT_KEY_NAME_CITY", ()))
		popup.setBodyString(CyTranslator().getText("TXT_KEY_SETTLE_NEW_CITY_NAME", ()))
		popup.createEditBox(city.getName())
		popup.setEditBoxMaxCharCount(15)
		popup.launch()



	def __eventEditCityNameApply(self, playerID, userData, popupReturn):
		city = gc.getPlayer(userData[2]).getCity(userData[0])
		cityName = popupReturn.getEditBoxString(0)

	### Dynamic City Naming
		HR_Cities.renameCustom(city, cityName)
		city.setName(cityName, not userData[1])
		###

		if CyGame().GetWorldBuilderMode() and not CyGame().isInAdvancedStart():
			WBCityEditScreen.WBCityEditScreen().placeStats()



	def __eventEditUnitNameBegin(self, argsList):
		pUnit = argsList
		popup = PyPopup.PyPopup(CvUtil.EventEditUnitName, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setUserData((pUnit.getID(), CyGame().getActivePlayer()))
		popup.setBodyString(CyTranslator().getText("TXT_KEY_RENAME_UNIT", ()))
		popup.createEditBox(pUnit.getNameNoDesc())
		popup.setEditBoxMaxCharCount(25)
		popup.launch()



	def __eventEditUnitNameApply(self, playerID, userData, popupReturn):
		unit = gc.getPlayer(userData[1]).getUnit(userData[0])
		newName = popupReturn.getEditBoxString(0)
		unit.setName(newName)
		if CyGame().GetWorldBuilderMode():
			WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeStats()
			WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeCurrentUnit()



	def __eventWBScriptPopupBegin(self):
		return



	def __eventWBGameScriptPopupApply(self, playerID, userData, popupReturn):
		sScript = popupReturn.getEditBoxString(0)
		CyGame().setScriptData(CvUtil.convertToStr(sScript))
		WBGameDataScreen.WBGameDataScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
		return



	def __eventWBPlayerScriptPopupApply(self, playerID, userData, popupReturn):
		sScript = popupReturn.getEditBoxString(0)
		gc.getPlayer(userData[0]).setScriptData(CvUtil.convertToStr(sScript))
		WBPlayerScreen.WBPlayerScreen().placeScript()
		return



	def __eventWBCityScriptPopupApply(self, playerID, userData, popupReturn):
		sScript = popupReturn.getEditBoxString(0)
		pCity = gc.getPlayer(userData[0]).getCity(userData[1])
		pCity.setScriptData(CvUtil.convertToStr(sScript))
		WBCityEditScreen.WBCityEditScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
		return



	def __eventWBUnitScriptPopupApply(self, playerID, userData, popupReturn):
		sScript = popupReturn.getEditBoxString(0)
		pUnit = gc.getPlayer(userData[0]).getUnit(userData[1])
		pUnit.setScriptData(CvUtil.convertToStr(sScript))
		WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
		return



	def __eventWBPlotScriptPopupApply(self, playerID, userData, popupReturn):
		sScript = popupReturn.getEditBoxString(0)
		pPlot = CyMap().plot(userData[0], userData[1])
		pPlot.setScriptData(CvUtil.convertToStr(sScript))
		WBPlotScreen.WBPlotScreen().placeScript()
		return



	def __eventWBLandmarkPopupApply(self, playerID, userData, popupReturn):
		sScript = popupReturn.getEditBoxString(0)
		pPlot = CyMap().plot(userData[0], userData[1])
		iPlayer = userData[2]
		if userData[3] > -1:
			pSign = CyEngine().getSignByIndex(userData[3])
			iPlayer = pSign.getPlayerType()
			CyEngine().removeSign(pPlot, iPlayer)
		if len(sScript):
			if iPlayer == gc.getBARBARIAN_PLAYER():
				CyEngine().addLandmark(pPlot, CvUtil.convertToStr(sScript))
			else:
				CyEngine().addSign(pPlot, iPlayer, CvUtil.convertToStr(sScript))
		WBPlotScreen.iCounter = 10
		return