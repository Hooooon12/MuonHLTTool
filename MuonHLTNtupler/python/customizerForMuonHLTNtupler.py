# -- custoimzer for ntupler that can be added to the HLT configuration for re-running HLT
# -- add two lines in the HLT config.:
# from MuonHLTTool.MuonHLTNtupler.customizerForMuonHLTNtupler import *
# process = customizerFuncForMuonHLTNtupler(process, "MYHLT")

import FWCore.ParameterSet.Config as cms
import HLTrigger.MuonHLTSeedMVAClassifier.mvaScale as _mvaScale

def customizerFuncForMuonHLTNtupler(process, newProcessName = "MYHLT", doDYSkim = False, MvaVersion = "Run3v0"):
    if hasattr(process, "DQMOutput"):
        del process.DQMOutput


    from MuonHLTTool.MuonHLTNtupler.ntupler_cfi import ntuplerBase
    import SimTracker.TrackAssociatorProducers.quickTrackAssociatorByHits_cfi
    from SimTracker.TrackerHitAssociation.tpClusterProducer_cfi import tpClusterProducer as _tpClusterProducer

    process.hltTPClusterProducer = _tpClusterProducer.clone(
      pixelClusterSrc = "hltSiPixelClusters",
      stripClusterSrc = "hltSiStripRawToClustersFacility"
    )
    # process.hltTPClusterProducer.pixelSimLinkSrc = cms.InputTag("simSiPixelDigis","Pixel")
    process.hltTrackAssociatorByHits = SimTracker.TrackAssociatorProducers.quickTrackAssociatorByHits_cfi.quickTrackAssociatorByHits.clone()
    process.hltTrackAssociatorByHits.cluster2TPSrc            = cms.InputTag("hltTPClusterProducer")
    process.hltTrackAssociatorByHits.UseGrouped               = cms.bool( False )
    process.hltTrackAssociatorByHits.UseSplitting             = cms.bool( False )
    process.hltTrackAssociatorByHits.ThreeHitTracksAreSpecial = cms.bool( False )

    # -- track - TP associations
    import SimMuon.MCTruth.MuonTrackProducer_cfi
    process.hltIterL3MuonsNoIDTracks = SimMuon.MCTruth.MuonTrackProducer_cfi.muonTrackProducer.clone()
    process.hltIterL3MuonsNoIDTracks.muonsTag                      = cms.InputTag("hltIterL3MuonsNoID")
    process.hltIterL3MuonsNoIDTracks.selectionTags                 = ('All',)
    process.hltIterL3MuonsNoIDTracks.trackType                     = "recomuonTrack"
    process.hltIterL3MuonsNoIDTracks.ignoreMissingMuonCollection   = True
    process.hltIterL3MuonsNoIDTracks.inputCSCSegmentCollection     = cms.InputTag("hltCscSegments")
    process.hltIterL3MuonsNoIDTracks.inputDTRecSegment4DCollection = cms.InputTag("hltDt4DSegments")

    process.hltIterL3MuonsTracks = SimMuon.MCTruth.MuonTrackProducer_cfi.muonTrackProducer.clone()
    process.hltIterL3MuonsTracks.muonsTag                          = cms.InputTag("hltIterL3Muons")
    process.hltIterL3MuonsTracks.selectionTags                     = ('All',)
    process.hltIterL3MuonsTracks.trackType                         = "recomuonTrack"
    process.hltIterL3MuonsTracks.ignoreMissingMuonCollection       = True
    process.hltIterL3MuonsTracks.inputCSCSegmentCollection         = cms.InputTag("hltCscSegments")
    process.hltIterL3MuonsTracks.inputDTRecSegment4DCollection     = cms.InputTag("hltDt4DSegments")

    from SimMuon.MCTruth.MuonAssociatorByHits_cfi import muonAssociatorByHits as _muonAssociatorByHits
    hltMuonAssociatorByHits = _muonAssociatorByHits.clone()
    hltMuonAssociatorByHits.PurityCut_track              = 0.75
    hltMuonAssociatorByHits.PurityCut_muon               = 0.75
    hltMuonAssociatorByHits.DTrechitTag                  = 'hltDt1DRecHits'
    hltMuonAssociatorByHits.ignoreMissingTrackCollection = True
    hltMuonAssociatorByHits.UseTracker                   = True
    hltMuonAssociatorByHits.UseMuon                      = True

    process.AhltIterL3OIMuonTrackSelectionHighPurity            = hltMuonAssociatorByHits.clone( tracksTag = 'hltIterL3OIMuonTrackSelectionHighPurity' )
    process.AhltIter0IterL3MuonTrackSelectionHighPurity = hltMuonAssociatorByHits.clone( tracksTag = 'hltIter0IterL3MuonTrackSelectionHighPurity' )
    process.AhltIter2IterL3MuonTrackSelectionHighPurity = hltMuonAssociatorByHits.clone( tracksTag = 'hltIter2IterL3MuonTrackSelectionHighPurity' )
    process.AhltIter0IterL3FromL1MuonTrackSelectionHighPurity = hltMuonAssociatorByHits.clone( tracksTag = 'hltIter0IterL3FromL1MuonTrackSelectionHighPurity' )
    process.AhltIter2IterL3FromL1MuonTrackSelectionHighPurity = hltMuonAssociatorByHits.clone( tracksTag = 'hltIter2IterL3FromL1MuonTrackSelectionHighPurity' )
    process.AhltIter2IterL3MuonMerged                   = hltMuonAssociatorByHits.clone( tracksTag = 'hltIter2IterL3MuonMerged' )
    process.AhltIter2IterL3FromL1MuonMerged                   = hltMuonAssociatorByHits.clone( tracksTag = 'hltIter2IterL3FromL1MuonMerged' )
    process.AhltIterL3MuonMerged                   = hltMuonAssociatorByHits.clone( tracksTag = 'hltIterL3MuonMerged' )
    process.AhltIterL3MuonAndMuonFromL1Merged                   = hltMuonAssociatorByHits.clone( tracksTag = 'hltIterL3MuonAndMuonFromL1Merged' )
    process.AhltIterL3MuonsNoID                                 = hltMuonAssociatorByHits.clone( tracksTag = 'hltIterL3MuonsNoIDTracks' )
    process.AhltIterL3Muons                                     = hltMuonAssociatorByHits.clone( tracksTag = 'hltIterL3MuonsTracks' )

    trackNames = [
        'hltIterL3OIMuonTrackAssociated',
        'hltIter0IterL3MuonTrackAssociated',
        'hltIter2IterL3MuonTrackAssociated',
        'hltIter0IterL3FromL1MuonTrackAssociated',
        'hltIter2IterL3FromL1MuonTrackAssociated',
        'hltIter2IterL3MuonMergedAssociated',
        'hltIter2IterL3FromL1MuonMergedAssociated',
        'hltIterL3MuonMergedAssociated',
        'hltIterL3MuonAndMuonFromL1MergedAssociated',
        'iterL3MuonNoIDTrackAssociated',
        'iterL3MuonTrackAssociated'
    ]

    trackLabels = [
        'hltIterL3OIMuonTrackSelectionHighPurity',
        'hltIter0IterL3MuonTrackSelectionHighPurity',
        'hltIter2IterL3MuonTrackSelectionHighPurity',
        'hltIter0IterL3FromL1MuonTrackSelectionHighPurity',
        'hltIter2IterL3FromL1MuonTrackSelectionHighPurity',
        'hltIter2IterL3MuonMerged',
        'hltIter2IterL3FromL1MuonMerged',
        'hltIterL3MuonMerged',
        'hltIterL3MuonAndMuonFromL1Merged',
        'hltIterL3MuonsNoIDTracks',
        'hltIterL3MuonsTracks'
    ]

    assoLabels = [
        'AhltIterL3OIMuonTrackSelectionHighPurity',
        'AhltIter0IterL3MuonTrackSelectionHighPurity',
        'AhltIter2IterL3MuonTrackSelectionHighPurity',
        'AhltIter0IterL3FromL1MuonTrackSelectionHighPurity',
        'AhltIter2IterL3FromL1MuonTrackSelectionHighPurity',
        'AhltIter2IterL3MuonMerged',
        'AhltIter2IterL3FromL1MuonMerged',
        'AhltIterL3MuonMerged',
        'AhltIterL3MuonAndMuonFromL1Merged',
        'AhltIterL3MuonsNoID',
        'AhltIterL3Muons'
    ]

    process.trackAssoSeq = cms.Sequence(
        process.hltIterL3MuonsNoIDTracks +
        process.hltIterL3MuonsTracks +
        process.AhltIterL3OIMuonTrackSelectionHighPurity +
        process.AhltIter0IterL3MuonTrackSelectionHighPurity +
        process.AhltIter2IterL3MuonTrackSelectionHighPurity +
        process.AhltIter0IterL3FromL1MuonTrackSelectionHighPurity +
        process.AhltIter2IterL3FromL1MuonTrackSelectionHighPurity +
        process.AhltIter2IterL3MuonMerged +
        process.AhltIter2IterL3FromL1MuonMerged +
        process.AhltIterL3MuonMerged +
        process.AhltIterL3MuonAndMuonFromL1Merged +
        process.AhltIterL3MuonsNoID +
        process.AhltIterL3Muons
    ) #JH

    # -- L1 Trigger matching
    from MuonAnalysis.MuonAssociators.muonL1Match_cfi import muonL1Match as _muonL1Match
    process.muonL1Info = _muonL1Match.clone(
        src = cms.InputTag("genParticles"),
        useMB2InOverlap = cms.bool(True),
        useStage2L1 = cms.bool(True),
        preselection = cms.string(""),
        matched = cms.InputTag("hltGtStage2Digis:Muon:"),
        useTrack = cms.string("none")
    )
    process.muonL1InfoByQ = process.muonL1Info.clone(
        sortBy = cms.string("quality"),
        sortByQual     = cms.bool(True), #JH : see MuonAnalysis/MuonAssociators/src/L1MuonMatcherAlgo.cc
        sortByDeltaPhi = cms.bool(False),
        sortByDeltaEta = cms.bool(False),
        sortByPt       = cms.bool(False)
    )

    process.L1AssoSeq = cms.Sequence(
        process.muonL1Info +
        process.muonL1InfoByQ
    ) #JH

    process.ntupler = ntuplerBase.clone()

    process.ntupler.trackCollectionNames  = cms.untracked.vstring(   trackNames )
    process.ntupler.trackCollectionLabels = cms.untracked.VInputTag( trackLabels )
    process.ntupler.associationLabels     = cms.untracked.VInputTag( assoLabels ) #JH

    process.ntupler.genParticles = cms.InputTag("genParticles")
    process.ntupler.l1Matches = cms.InputTag("muonL1Info")
    process.ntupler.l1MatchesQuality = cms.InputTag("muonL1Info", "quality")
    process.ntupler.l1MatchesDeltaR = cms.InputTag("muonL1Info", "deltaR")
    process.ntupler.l1MatchesByQ = cms.InputTag("muonL1InfoByQ")
    process.ntupler.l1MatchesByQQuality = cms.InputTag("muonL1InfoByQ", "quality")
    process.ntupler.l1MatchesByQDeltaR = cms.InputTag("muonL1InfoByQ", "deltaR") #JH

    # -- set to the new process name
    process.ntupler.myTriggerResults = cms.untracked.InputTag("TriggerResults",          "",     newProcessName)
    process.ntupler.myTriggerEvent   = cms.untracked.InputTag("hltTriggerSummaryAOD",    "",     newProcessName)
    process.ntupler.lumiScaler       = cms.untracked.InputTag("hltScalersRawToDigi",     "",     newProcessName)

    process.ntupler.L1Muon           = cms.untracked.InputTag("hltGtStage2Digis",        "Muon", newProcessName)
    # process.ntupler.L1Muon           = cms.untracked.InputTag("gmtStage2Digis",        "Muon", newProcessName) 
    # process.ntupler.L1Muon           = cms.untracked.InputTag("hltGtStage2Digis",        "Muon", "HLT") #for phaseII w/o emulation
    # process.ntupler.L1Muon           = cms.untracked.InputTag("simGmtStage2Digis","",newProcessName)  # Phase II sim emul
    process.ntupler.L2Muon           = cms.untracked.InputTag("hltL2MuonCandidates",     "",     newProcessName)
    process.ntupler.L3Muon           = cms.untracked.InputTag("hltIterL3MuonCandidates", "",     newProcessName)
    process.ntupler.TkMuon           = cms.untracked.InputTag("hltHighPtTkMuonCands",    "",     newProcessName)

    process.ntupler.iterL3OI         = cms.untracked.InputTag("hltL3MuonsIterL3OI",                   "", newProcessName)
    process.ntupler.iterL3IOFromL2   = cms.untracked.InputTag("hltL3MuonsIterL3IO",                   "", newProcessName)
    process.ntupler.iterL3FromL2     = cms.untracked.InputTag("hltIterL3MuonsFromL2LinksCombination", "", newProcessName)
    process.ntupler.iterL3IOFromL1   = cms.untracked.InputTag("hltIter3IterL3FromL1MuonMerged",       "", newProcessName)
    process.ntupler.iterL3MuonNoID   = cms.untracked.InputTag("hltIterL3MuonsNoID",                   "", newProcessName)
    process.ntupler.iterL3Muon       = cms.untracked.InputTag("hltIterL3Muons",                       "", newProcessName)

    process.ntupler.hltIterL3MuonTrimmedPixelVertices                 = cms.untracked.InputTag("hltIterL3MuonTrimmedPixelVertices",                   "", newProcessName)
    process.ntupler.hltIterL3FromL1MuonTrimmedPixelVertices           = cms.untracked.InputTag("hltIterL3FromL1MuonTrimmedPixelVertices",             "", newProcessName)

    process.ntupler.doMVA  = cms.bool(True)
    process.ntupler.doSeed = cms.bool(False)

    process.ntupler.hltIterL3OISeedsFromL2Muons                       = cms.untracked.InputTag("hltIterL3OISeedsFromL2Muons",                         "", newProcessName)
    process.ntupler.hltIter0IterL3MuonPixelSeedsFromPixelTracks       = cms.untracked.InputTag("hltIter0IterL3MuonPixelSeedsFromPixelTracks",         "", newProcessName)
    process.ntupler.hltIter2IterL3MuonPixelSeeds                      = cms.untracked.InputTag("hltIter2IterL3MuonPixelSeeds",                        "", newProcessName)
    process.ntupler.hltIter3IterL3MuonPixelSeeds                      = cms.untracked.InputTag("hltIter3IterL3MuonPixelSeeds",                        "", newProcessName)
    process.ntupler.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks = cms.untracked.InputTag("hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks",   "", newProcessName)
    process.ntupler.hltIter2IterL3FromL1MuonPixelSeeds                = cms.untracked.InputTag("hltIter2IterL3FromL1MuonPixelSeeds",                  "", newProcessName)
    process.ntupler.hltIter3IterL3FromL1MuonPixelSeeds                = cms.untracked.InputTag("hltIter3IterL3FromL1MuonPixelSeeds",                  "", newProcessName)

    process.ntupler.hltIterL3OIMuonTrack                              = cms.untracked.InputTag("hltIterL3OIMuonTrackSelectionHighPurity",             "", newProcessName)
    process.ntupler.hltIter0IterL3MuonTrack                           = cms.untracked.InputTag("hltIter0IterL3MuonTrackSelectionHighPurity",          "", newProcessName)
    process.ntupler.hltIter2IterL3MuonTrack                           = cms.untracked.InputTag("hltIter2IterL3MuonTrackSelectionHighPurity",          "", newProcessName)
    process.ntupler.hltIter3IterL3MuonTrack                           = cms.untracked.InputTag("hltIter3IterL3MuonTrackSelectionHighPurity",          "", newProcessName)
    process.ntupler.hltIter0IterL3FromL1MuonTrack                     = cms.untracked.InputTag("hltIter0IterL3FromL1MuonTrackSelectionHighPurity",    "", newProcessName)
    process.ntupler.hltIter2IterL3FromL1MuonTrack                     = cms.untracked.InputTag("hltIter2IterL3FromL1MuonTrackSelectionHighPurity",    "", newProcessName)
    process.ntupler.hltIter3IterL3FromL1MuonTrack                     = cms.untracked.InputTag("hltIter3IterL3FromL1MuonTrackSelectionHighPurity",    "", newProcessName)

    # process.ntupler.associatePixel = cms.bool(True)
    # process.ntupler.associateRecoTracks = cms.bool(False)
    # process.ntupler.associateStrip = cms.bool(True)
    # process.ntupler.pixelSimLinkSrc = cms.InputTag("simSiPixelDigis","Pixel")
    # process.ntupler.stripSimLinkSrc = cms.InputTag("simSiStripDigis")
    # process.ntupler.ROUList = cms.vstring('g4SimHitsTrackerHitsPixelBarrelLowTof', 'g4SimHitsTrackerHitsPixelBarrelHighTof', 'g4SimHitsTrackerHitsPixelEndcapLowTof', 'g4SimHitsTrackerHitsPixelEndcapHighTof')
    # process.ntupler.usePhase2Tracker = cms.bool(True)
    # process.ntupler.phase2TrackerSimLinkSrc = cms.InputTag("simSiPixelDigis","Tracker")

    process.ntupler.associator = cms.untracked.InputTag("hltTrackAssociatorByHits")
    process.ntupler.trackingParticle = cms.untracked.InputTag("mix","MergedTrackTruth")


    #process.ntupler.mvaFileHltIterL3OISeedsFromL2Muons_B_0                       = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIterL3OI_0.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIterL3OISeedsFromL2Muons_B_1                       = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIterL3OI_1.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIterL3OISeedsFromL2Muons_B_2                       = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIterL3OI_2.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIterL3OISeedsFromL2Muons_B_3                       = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIterL3OI_3.xml" % MvaVersion)
    # process.ntupler.mvaFileHltIter0IterL3MuonPixelSeedsFromPixelTracks_B_0       = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter0_0.xml" % MvaVersion)
    # process.ntupler.mvaFileHltIter0IterL3MuonPixelSeedsFromPixelTracks_B_1       = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter0_1.xml" % MvaVersion)
    # process.ntupler.mvaFileHltIter0IterL3MuonPixelSeedsFromPixelTracks_B_2       = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter0_2.xml" % MvaVersion)
    # process.ntupler.mvaFileHltIter0IterL3MuonPixelSeedsFromPixelTracks_B_3       = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter0_3.xml" % MvaVersion)
    process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_B                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter2.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_B_0                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter2_0.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_B_1                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter2_1.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_B_2                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter2_2.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_B_3                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter2_3.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter3IterL3MuonPixelSeeds_B_0                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter3_0.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter3IterL3MuonPixelSeeds_B_1                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter3_1.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter3IterL3MuonPixelSeeds_B_2                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter3_2.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter3IterL3MuonPixelSeeds_B_3                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter3_3.xml" % MvaVersion)
    # process.ntupler.mvaFileHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_B_0 = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter0FromL1_0.xml" % MvaVersion)
    # process.ntupler.mvaFileHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_B_1 = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter0FromL1_1.xml" % MvaVersion)
    # process.ntupler.mvaFileHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_B_2 = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter0FromL1_2.xml" % MvaVersion)
    # process.ntupler.mvaFileHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_B_3 = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter0FromL1_3.xml" % MvaVersion)
    process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_B                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter2FromL1.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_B_0                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter2FromL1_0.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_B_1                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter2FromL1_1.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_B_2                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter2FromL1_2.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_B_3                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter2FromL1_3.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter3IterL3FromL1MuonPixelSeeds_B_0                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter3FromL1_0.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter3IterL3FromL1MuonPixelSeeds_B_1                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter3FromL1_1.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter3IterL3FromL1MuonPixelSeeds_B_2                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter3FromL1_2.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter3IterL3FromL1MuonPixelSeeds_B_3                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Barrel_hltIter3FromL1_3.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIterL3OISeedsFromL2Muons_E_0                       = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIterL3OI_0.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIterL3OISeedsFromL2Muons_E_1                       = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIterL3OI_1.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIterL3OISeedsFromL2Muons_E_2                       = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIterL3OI_2.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIterL3OISeedsFromL2Muons_E_3                       = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIterL3OI_3.xml" % MvaVersion)
    # process.ntupler.mvaFileHltIter0IterL3MuonPixelSeedsFromPixelTracks_E_0       = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter0_0.xml" % MvaVersion)
    # process.ntupler.mvaFileHltIter0IterL3MuonPixelSeedsFromPixelTracks_E_1       = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter0_1.xml" % MvaVersion)
    # process.ntupler.mvaFileHltIter0IterL3MuonPixelSeedsFromPixelTracks_E_2       = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter0_2.xml" % MvaVersion)
    # process.ntupler.mvaFileHltIter0IterL3MuonPixelSeedsFromPixelTracks_E_3       = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter0_3.xml" % MvaVersion)
    process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_E                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter2.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_E_0                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter2_0.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_E_1                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter2_1.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_E_2                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter2_2.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_E_3                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter2_3.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter3IterL3MuonPixelSeeds_E_0                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter3_0.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter3IterL3MuonPixelSeeds_E_1                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter3_1.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter3IterL3MuonPixelSeeds_E_2                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter3_2.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter3IterL3MuonPixelSeeds_E_3                      = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter3_3.xml" % MvaVersion)
    # process.ntupler.mvaFileHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_E_0 = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter0FromL1_0.xml" % MvaVersion)
    # process.ntupler.mvaFileHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_E_1 = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter0FromL1_1.xml" % MvaVersion)
    # process.ntupler.mvaFileHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_E_2 = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter0FromL1_2.xml" % MvaVersion)
    # process.ntupler.mvaFileHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_E_3 = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter0FromL1_3.xml" % MvaVersion)
    process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_E                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter2FromL1.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_E_0                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter2FromL1_0.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_E_1                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter2FromL1_1.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_E_2                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter2FromL1_2.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_E_3                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter2FromL1_3.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter3IterL3FromL1MuonPixelSeeds_E_0                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter3FromL1_0.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter3IterL3FromL1MuonPixelSeeds_E_1                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter3FromL1_1.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter3IterL3FromL1MuonPixelSeeds_E_2                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter3FromL1_2.xml" % MvaVersion)
    #process.ntupler.mvaFileHltIter3IterL3FromL1MuonPixelSeeds_E_3                = cms.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/%s_Endcap_hltIter3FromL1_3.xml" % MvaVersion)


    #process.ntupler.mvaScaleMeanHltIterL3OISeedsFromL2Muons_B                       = cms.vdouble( getattr(_mvaScale, "%s_Barrel_hltIterL3OI_ScaleMean" % MvaVersion) )
    #process.ntupler.mvaScaleStdHltIterL3OISeedsFromL2Muons_B                        = cms.vdouble( getattr(_mvaScale, "%s_Barrel_hltIterL3OI_ScaleStd" % MvaVersion) )
    # process.ntupler.mvaScaleMeanHltIter0IterL3MuonPixelSeedsFromPixelTracks_B       = cms.vdouble( getattr(_mvaScale, "%s_Barrel_hltIter0_ScaleMean" % MvaVersion) )
    # process.ntupler.mvaScaleStdHltIter0IterL3MuonPixelSeedsFromPixelTracks_B        = cms.vdouble( getattr(_mvaScale, "%s_Barrel_hltIter0_ScaleStd" % MvaVersion) )
    process.ntupler.mvaScaleMeanHltIter2IterL3MuonPixelSeeds_B                      = cms.vdouble( getattr(_mvaScale, "%s_Barrel_hltIter2_ScaleMean" % MvaVersion) )
    process.ntupler.mvaScaleStdHltIter2IterL3MuonPixelSeeds_B                       = cms.vdouble( getattr(_mvaScale, "%s_Barrel_hltIter2_ScaleStd" % MvaVersion) )
    #process.ntupler.mvaScaleMeanHltIter3IterL3MuonPixelSeeds_B                      = cms.vdouble( getattr(_mvaScale, "%s_Barrel_hltIter3_ScaleMean" % MvaVersion) )
    #process.ntupler.mvaScaleStdHltIter3IterL3MuonPixelSeeds_B                       = cms.vdouble( getattr(_mvaScale, "%s_Barrel_hltIter3_ScaleStd" % MvaVersion) )
    # process.ntupler.mvaScaleMeanHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_B = cms.vdouble( getattr(_mvaScale, "%s_Barrel_hltIter0FromL1_ScaleMean" % MvaVersion) )
    # process.ntupler.mvaScaleStdHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_B  = cms.vdouble( getattr(_mvaScale, "%s_Barrel_hltIter0FromL1_ScaleStd" % MvaVersion) )
    process.ntupler.mvaScaleMeanHltIter2IterL3FromL1MuonPixelSeeds_B                = cms.vdouble( getattr(_mvaScale, "%s_Barrel_hltIter2FromL1_ScaleMean" % MvaVersion) )
    process.ntupler.mvaScaleStdHltIter2IterL3FromL1MuonPixelSeeds_B                 = cms.vdouble( getattr(_mvaScale, "%s_Barrel_hltIter2FromL1_ScaleStd" % MvaVersion) )
    #process.ntupler.mvaScaleMeanHltIter3IterL3FromL1MuonPixelSeeds_B                = cms.vdouble( getattr(_mvaScale, "%s_Barrel_hltIter3FromL1_ScaleMean" % MvaVersion) )
    #process.ntupler.mvaScaleStdHltIter3IterL3FromL1MuonPixelSeeds_B                 = cms.vdouble( getattr(_mvaScale, "%s_Barrel_hltIter3FromL1_ScaleStd" % MvaVersion) )
    #process.ntupler.mvaScaleMeanHltIterL3OISeedsFromL2Muons_E                       = cms.vdouble( getattr(_mvaScale, "%s_Endcap_hltIterL3OI_ScaleMean" % MvaVersion) )
    #process.ntupler.mvaScaleStdHltIterL3OISeedsFromL2Muons_E                        = cms.vdouble( getattr(_mvaScale, "%s_Endcap_hltIterL3OI_ScaleStd" % MvaVersion) )
    # process.ntupler.mvaScaleMeanHltIter0IterL3MuonPixelSeedsFromPixelTracks_E       = cms.vdouble( getattr(_mvaScale, "%s_Endcap_hltIter0_ScaleMean" % MvaVersion) )
    # process.ntupler.mvaScaleStdHltIter0IterL3MuonPixelSeedsFromPixelTracks_E        = cms.vdouble( getattr(_mvaScale, "%s_Endcap_hltIter0_ScaleStd" % MvaVersion) )
    process.ntupler.mvaScaleMeanHltIter2IterL3MuonPixelSeeds_E                      = cms.vdouble( getattr(_mvaScale, "%s_Endcap_hltIter2_ScaleMean" % MvaVersion) )
    process.ntupler.mvaScaleStdHltIter2IterL3MuonPixelSeeds_E                       = cms.vdouble( getattr(_mvaScale, "%s_Endcap_hltIter2_ScaleStd" % MvaVersion) )
    #process.ntupler.mvaScaleMeanHltIter3IterL3MuonPixelSeeds_E                      = cms.vdouble( getattr(_mvaScale, "%s_Endcap_hltIter3_ScaleMean" % MvaVersion) )
    #process.ntupler.mvaScaleStdHltIter3IterL3MuonPixelSeeds_E                       = cms.vdouble( getattr(_mvaScale, "%s_Endcap_hltIter3_ScaleStd" % MvaVersion) )
    # process.ntupler.mvaScaleMeanHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_E = cms.vdouble( getattr(_mvaScale, "%s_Endcap_hltIter0FromL1_ScaleMean" % MvaVersion) )
    # process.ntupler.mvaScaleStdHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_E  = cms.vdouble( getattr(_mvaScale, "%s_Endcap_hltIter0FromL1_ScaleStd" % MvaVersion) )
    process.ntupler.mvaScaleMeanHltIter2IterL3FromL1MuonPixelSeeds_E                = cms.vdouble( getattr(_mvaScale, "%s_Endcap_hltIter2FromL1_ScaleMean" % MvaVersion) )
    process.ntupler.mvaScaleStdHltIter2IterL3FromL1MuonPixelSeeds_E                 = cms.vdouble( getattr(_mvaScale, "%s_Endcap_hltIter2FromL1_ScaleStd" % MvaVersion) )
    #process.ntupler.mvaScaleMeanHltIter3IterL3FromL1MuonPixelSeeds_E                = cms.vdouble( getattr(_mvaScale, "%s_Endcap_hltIter3FromL1_ScaleMean" % MvaVersion) )
    #process.ntupler.mvaScaleStdHltIter3IterL3FromL1MuonPixelSeeds_E                 = cms.vdouble( getattr(_mvaScale, "%s_Endcap_hltIter3FromL1_ScaleStd" % MvaVersion) )



    process.TFileService = cms.Service("TFileService",
      fileName = cms.string("ntuple.root"),
      closeFileFast = cms.untracked.bool(False),
    )

    process.ntupler.myTriggerResults = cms.untracked.InputTag("TriggerResults::HLT") # dummy to avoid ordering error occur in skimming, as it is not used at the moment

    # L1TRK_PROC  =  process.TTTracksFromTrackletEmulation
    # L1TRK_NAME  = "TTTracksFromTrackletEmulation"
    # L1TRK_LABEL = "Level1TTTracks"
    # process.TTTrackAssociatorFromPixelDigis.TTTracks = cms.VInputTag( cms.InputTag("TTTracksFromTrackletEmulation", "Level1TTTracks") )

    process.ntupler.DebugMode = cms.bool(False)
    # process.ntupler.SaveAllTracks = cms.bool(True)
    # process.ntupler.SaveStubs = cms.bool(False)
    # process.ntupler.L1TrackInputTag = cms.InputTag(L1TRK_NAME, L1TRK_LABEL) # TTTrack input 
    # process.ntupler.MCTruthTrackInputTag = cms.InputTag("TTTrackAssociatorFromPixelDigis", L1TRK_LABEL)  ## MCTruth input
    # process.ntupler.L1StubInputTag = cms.InputTag("TTStubsFromPhase2TrackerDigis","StubAccepted")
    # process.ntupler.TkMuonToken = cms.InputTag("L1TkMuons","")
    # process.ntupler.l1TkPrimaryVertex = cms.InputTag("L1TkPrimaryVertex","")

    if doDYSkim:
        from MuonHLTTool.MuonHLTNtupler.DYmuSkimmer import DYmuSkimmer 
        process.Skimmer = DYmuSkimmer.clone()
        process.mypath = cms.Path(process.Skimmer*process.hltTPClusterProducer*process.hltTrackAssociatorByHits*process.trackAssoSeq*process.L1AssoSeq*process.ntupler)
    else:
        process.mypath = cms.Path(process.hltTPClusterProducer*process.hltTrackAssociatorByHits*process.trackAssoSeq*process.L1AssoSeq*process.ntupler) #JH

    return process
