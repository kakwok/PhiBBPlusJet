import os
import sys
from ROOT import *
import DAZSLE.PhiBBPlusJet.analysis_configuration as config

if "uscms" in os.path.expandvars("$HOME"):
    idir = "root://cmseos.fnal.gov//eos/uscms/store/user/lpchbb/zprimebits-v12.04/norm2/cvernier/"
    idir_muon = "root://cmseos.fnal.gov//eos/uscms/store/user/lpchbb/zprimebits-v12.04/cvernier/"
    idir_data = 'root://cmseos.fnal.gov//eos/uscms/store/user/lpchbb/zprimebits-v12.05/'
    tfiles = {
    ############### Signals
              'Sbb50': [idir_data + '/Spin0_ggPhibb1j_g1_50_Scalar_1000pb_weighted.root'],
              'Sbb100': [idir_data + '/Spin0_ggPhibb1j_g1_100_Scalar_1000pb_weighted.root'],
              'Sbb125': [idir_data + '/Spin0_ggPhibb1j_g1_125_Scalar_1000pb_weighted.root'],
              'Sbb200': [idir_data + '/Spin0_ggPhibb1j_g1_200_Scalar_1000pb_weighted.root'],
              'Sbb300': [idir_data + '/Spin0_ggPhibb1j_g1_300_Scalar_1000pb_weighted.root'],
              'Sbb350': [idir_data + '/Spin0_ggPhibb1j_g1_350_Scalar_1000pb_weighted.root'],
              'Sbb400': [idir_data + '/Spin0_ggPhibb1j_g1_400_Scalar_1000pb_weighted.root'],
              'Sbb500': [idir_data + '/Spin0_ggPhibb1j_g1_500_Scalar_1000pb_weighted.root'],
    ############### Backgrounds
              'qcd': [idir_data + '/QCD_HT100to200_13TeV_1000pb_weighted.root',
                      idir_data + '/QCD_HT200to300_13TeV_1000pb_weighted.root',
                      idir_data + '/QCD_HT300to500_13TeV_all_1000pb_weighted.root',
                      idir_data + '/QCD_HT500to700_13TeV_1000pb_weighted.root',
                      idir_data + '/QCD_HT700to1000_13TeV_1000pb_weighted.root',
                      idir_data + '/QCD_HT1000to1500_13TeV_1000pb_weighted.root',
                      idir_data + '/QCD_HT1500to2000_13TeV_all_1000pb_weighted.root',
                      idir_data + '/QCD_HT2000toInf_13TeV_all_1000pb_weighted.root'],
              'wqq':  [idir_data + '/WJetsToQQ_HT180_13TeV_1000pb_weighted.root'],
              'tqq':  [idir + '/TT_powheg_1000pb_weighted.root'], #Powheg is the new default
              'zqq': [idir_data + '/DYJetsToQQ_HT180_13TeV_1000pb_weighted.root'],
              'stqq':  [idir + '/ST_t_channel_antitop_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV_powhegV2_madspin_1000pb_weighted.root',
                             idir + '/ST_t_channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV_powhegV2_madspin_1000pb_weighted.root',
                             idir + '/ST_tW_antitop_5f_inclusiveDecays_13TeV_powheg_pythia8_TuneCUETP8M2T4_1000pb_weighted.root',
                             idir + '/ST_tW_top_5f_inclusiveDecays_13TeV_powheg_pythia8_TuneCUETP8M2T4_1000pb_weighted.root'],
              'vvqq': [idir + '/WWTo4Q_13TeV_powheg_1000pb_weighted.root',
                          idir + '/ZZ_13TeV_pythia8_1000pb_weighted.root',#ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8_1000pb_weighted.root',
                          idir + '/WZ_13TeV_pythia8_1000pb_weighted.root'],
              'hbb':   [idir_data + '/GluGluHToBB_M125_13TeV_powheg_pythia8_CKKW_1000pb_weighted.root',
                      	idir + '/VBFHToBB_M_125_13TeV_powheg_pythia8_weightfix_all_1000pb_weighted.root',
                      	idir + '/ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8_1000pb_weighted.root',
                      	idir + '/WminusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8_1000pb_weighted.root',
                      	idir + '/WplusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8_1000pb_weighted.root',  
                      	idir + '/ttHTobb_M125_13TeV_powheg_pythia8_1000pb_weighted.root',
                      	idir + '/ggZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8_1000pb_weighted.root',
                      	idir + '/ggZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8_1000pb_weighted.root',
                      	idir + '/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8_ext_1000pb_weighted.root'],	
              'zll': [idir + '/DYJetsToLL_M_50_13TeV_ext_1000pb_weighted.root'],
              'wlnu': [idir + '/WJetsToLNu_HT_100To200_13TeV_1000pb_weighted.root',
                       idir + '/WJetsToLNu_HT_200To400_13TeV_1000pb_weighted.root',
                       idir + '/WJetsToLNu_HT_400To600_13TeV_1000pb_weighted.root',
                       idir + '/WJetsToLNu_HT_600To800_13TeV_1000pb_weighted.root',
                       idir + '/WJetsToLNu_HT_800To1200_13TeV_1000pb_weighted.root',
                       idir + '/WJetsToLNu_HT_1200To2500_13TeV_1000pb_weighted.root',
                       idir + '/WJetsToLNu_HT_2500ToInf_13TeV_1000pb_weighted.root'],
    ################
              'data_obs': [
         idir_data + 'JetHTRun2016B_03Feb2017_ver2_v2_v3.root',
         idir_data + 'JetHTRun2016B_03Feb2017_ver1_v1_v3.root',
                     idir_data + 'JetHTRun2016C_03Feb2017_v1_v3_0.root',
                     idir_data + 'JetHTRun2016C_03Feb2017_v1_v3_1.root',
                     idir_data + 'JetHTRun2016C_03Feb2017_v1_v3_2.root',
                     idir_data + 'JetHTRun2016C_03Feb2017_v1_v3_3.root',
                     idir_data + 'JetHTRun2016C_03Feb2017_v1_v3_4.root',
                     idir_data + 'JetHTRun2016C_03Feb2017_v1_v3_5.root',
                     idir_data + 'JetHTRun2016C_03Feb2017_v1_v3_6.root',
                     idir_data + 'JetHTRun2016C_03Feb2017_v1_v3_7.root',
                     idir_data + 'JetHTRun2016C_03Feb2017_v1_v3_8.root',
                     idir_data + 'JetHTRun2016C_03Feb2017_v1_v3_9.root',
                     idir_data + 'JetHTRun2016D_03Feb2017_v1_v3_0.root',
         idir_data + 'JetHTRun2016D_03Feb2017_v1_v3_1.root',
                     idir_data + 'JetHTRun2016D_03Feb2017_v1_v3_10.root',
                     idir_data + 'JetHTRun2016D_03Feb2017_v1_v3_11.root',
                     idir_data + 'JetHTRun2016D_03Feb2017_v1_v3_12.root',
                     idir_data + 'JetHTRun2016D_03Feb2017_v1_v3_13.root',
                     idir_data + 'JetHTRun2016D_03Feb2017_v1_v3_14.root',
                     idir_data + 'JetHTRun2016D_03Feb2017_v1_v3_2.root',
                     idir_data + 'JetHTRun2016D_03Feb2017_v1_v3_3.root',
                     idir_data + 'JetHTRun2016D_03Feb2017_v1_v3_4.root',
                     idir_data + 'JetHTRun2016D_03Feb2017_v1_v3_5.root',
                     idir_data + 'JetHTRun2016D_03Feb2017_v1_v3_6.root',
                     idir_data + 'JetHTRun2016D_03Feb2017_v1_v3_7.root',
                     idir_data + 'JetHTRun2016D_03Feb2017_v1_v3_8.root',
                     idir_data + 'JetHTRun2016D_03Feb2017_v1_v3_9.root',
                     idir_data + 'JetHTRun2016E_03Feb2017_v1_v3_0.root',
                     idir_data + 'JetHTRun2016E_03Feb2017_v1_v3_1.root',
                     idir_data + 'JetHTRun2016E_03Feb2017_v1_v3_2.root',
                     idir_data + 'JetHTRun2016E_03Feb2017_v1_v3_3.root',
                     idir_data + 'JetHTRun2016E_03Feb2017_v1_v3_4.root',
                     idir_data + 'JetHTRun2016E_03Feb2017_v1_v3_5.root',
                     idir_data + 'JetHTRun2016E_03Feb2017_v1_v3_6.root',
                     idir_data + 'JetHTRun2016E_03Feb2017_v1_v3_7.root',
                     idir_data + 'JetHTRun2016E_03Feb2017_v1_v3_8.root',
                     idir_data + 'JetHTRun2016E_03Feb2017_v1_v3_9.root',
                     idir_data + 'JetHTRun2016E_03Feb2017_v1_v3_10.root',
                     idir_data + 'JetHTRun2016E_03Feb2017_v1_v3_11.root',
                     idir_data + 'JetHTRun2016E_03Feb2017_v1_v3_12.root',
                     idir_data + 'JetHTRun2016E_03Feb2017_v1_v3_13.root',
                     idir_data + 'JetHTRun2016E_03Feb2017_v1_v3_14.root',
                     idir_data + 'JetHTRun2016F_03Feb2017_v1_v3_0.root',
                     idir_data + 'JetHTRun2016F_03Feb2017_v1_v3_1.root',
                     idir_data + 'JetHTRun2016F_03Feb2017_v1_v3_2.root',
                     idir_data + 'JetHTRun2016F_03Feb2017_v1_v3_3.root',
                     idir_data + 'JetHTRun2016F_03Feb2017_v1_v3_4.root',
                     idir_data + 'JetHTRun2016F_03Feb2017_v1_v3_5.root',
                     idir_data + 'JetHTRun2016F_03Feb2017_v1_v3_6.root',
                     idir_data + 'JetHTRun2016F_03Feb2017_v1_v3_7.root',
                     idir_data + 'JetHTRun2016F_03Feb2017_v1_v3_8.root',
                     idir_data + 'JetHTRun2016F_03Feb2017_v1_v3_9.root',
                     idir_data + 'JetHTRun2016F_03Feb2017_v1_v3_10.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_0.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_1.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_2.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_3.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_4.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_5.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_6.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_7.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_8.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_9.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_10.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_11.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_12.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_13.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_14.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_15.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_16.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_17.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_18.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_19.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_20.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_21.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_22.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_23.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_24.root',
                     idir_data + 'JetHTRun2016G_03Feb2017_v1_v3_25.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_0.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_1.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_2.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_3.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_4.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_5.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_6.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_7.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_8.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_9.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_10.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_11.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_12.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_13.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_14.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_15.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_16.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_17.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_18.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_19.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_20.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_21.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_22.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_23.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_24.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver2_v1_v3_25.root',
                     idir_data + 'JetHTRun2016H_03Feb2017_ver3_v1_v3.root'],
              'data_singlemu': [idir_muon + '/SingleMuonRun2016B_03Feb2017_ver1_v1_fixtrig.root',
                       idir_muon + '/SingleMuonRun2016B_03Feb2017_ver2_v2_fixtrig.root',
                       idir_muon + '/SingleMuonRun2016C_03Feb2017_v1_fixtrig.root',
                       idir_muon + '/SingleMuonRun2016D_03Feb2017_v1_fixtrig.root',
                       idir_muon + '/SingleMuonRun2016E_03Feb2017_v1_fixtrig.root',
                       idir_muon + '/SingleMuonRun2016F_03Feb2017_v1_fixtrig.root',
                       idir_muon + '/SingleMuonRun2016G_03Feb2017_v1_fixtrig.root',
                       idir_muon + '/SingleMuonRun2016H_03Feb2017_ver2_v1_fixtrig.root',
                       idir_muon + '/SingleMuonRun2016H_03Feb2017_ver3_v1_fixtrig.root']
            }
    anter_nevents = {}
    for sample_name in sorted(tfiles.keys()):
        anter_nevents[sample_name] = 0
        for filename in tfiles[sample_name]:
            f = TFile(filename, "READ")
            t = f.Get("otree")
            anter_nevents[sample_name] += t.GetEntriesFast()
            f.Close()

    print "Yours:"
    my_nevents = {}
    for supersample in sorted(tfiles.keys()):
        my_nevents[supersample] = 0
        for sample in config.samples[supersample]:
            if sample in config.sklims:
                for filename in config.sklims[sample]:
                    print "[debug] Openining " + filename
                    f = TFile.Open(filename, "READ")
                    t = f.Get("otree")
                    my_nevents[supersample] += t.GetEntriesFast()
                    f.Close()

    for supersample in sorted(tfiles.keys()):
        print "{} : {} | {}".format(supersample, anter_nevents[supersample], my_nevents[supersample])

else:
    my_nevents = {}
    for supersample in sorted(config.supersamples):
        my_nevents[supersample] = 0
        for sample in config.samples[supersample]:
            if sample in config.skims:
                for filename in config.skims[sample]:
                    print "[debug] Openining " + filename
                    f = TFile.Open(filename, "READ")
                    t = f.Get("otree")
                    my_nevents[supersample] += t.GetEntriesFast()
                    f.Close()

    for supersample in sorted(config.supersamples):
        print "{} : {}".format(supersample, my_nevents[supersample])
