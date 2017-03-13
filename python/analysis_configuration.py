import os

# Signal, background, data names
background_names = [
	"qcd",
	"stqq",
	"tqq",
	"wqq",
	"zqq",
	"vvqq",
]
signal_names = []
#signal_masses = [25,50,75,100,125,150,200,250,300,350,400,500,600,800]
signal_masses = [50,75,100,125,150,200,250,300,350,400,500,600,800,1000]
for mass in signal_masses:
	signal_names.append("Pbb_{}".format(mass))
data_names = ["data_obs"]
supersamples = []
supersamples.extend(background_names)
supersamples.extend(signal_names)
supersamples.extend(data_names)


# Sample names. Dictionary is [signal/background/data name]:[list of samples] 
samples = {
	"qcd":["QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"],
	"stqq":["ST_t_antitop","ST_t_top","ST_tW_antitop","ST_tW_top"],
	"tqq":["TTJets"],
	"wqq":["WJetsToQQ"],
	"zqq":["DYJetsToQQ"],
	"vvqq":["WWTo4Q", "WZ", "ZZ"],
	"data_obs":["JetHTRun2016B","JetHTRun2016C","JetHTRun2016D","JetHTRun2016E","JetHTRun2016F","JetHTRun2016G","JetHTRun2016H"],
	"Sbb_50":["Spin0_ggPhi12j_g1_50_Scalar"],
	"Sbb_75":["Spin0_ggPhi12j_g1_75_Scalar"],
	"Sbb_100":["Spin0_ggPhi12j_g1_100_Scalar"],
	"Sbb_125":["Spin0_ggPhi12j_g1_125_Scalar"],
	"Sbb_150":["Spin0_ggPhi12j_g1_150_Scalar"],
	"Sbb_250":["Spin0_ggPhi12j_g1_250_Scalar"],
	"Sbb_300":["Spin0_ggPhi12j_g1_300_Scalar"],
	"Sbb_400":["Spin0_ggPhi12j_g1_400_Scalar"],
	"Sbb_500":["Spin0_ggPhi12j_g1_500_Scalar"],
	"PSbb_50":["Spin0_ggPhi12j_g1_50_PseudoScalar"],
	"PSbb_75":["Spin0_ggPhi12j_g1_75_PseudoScalar"],
	"PSbb_100":["Spin0_ggPhi12j_g1_100_PseudoScalar"],
	"PSbb_125":["Spin0_ggPhi12j_g1_125_PseudoScalar"],
	"PSbb_150":["Spin0_ggPhi12j_g1_150_PseudoScalar"],
	"PSbb_250":["Spin0_ggPhi12j_g1_250_PseudoScalar"],
	"PSbb_300":["Spin0_ggPhi12j_g1_300_PseudoScalar"],
	"PSbb_400":["Spin0_ggPhi12j_g1_400_PseudoScalar"],
	"PSbb_500":["Spin0_ggPhi12j_g1_500_PseudoScalar"],
}
#for mass in signal_masses:
#	for spin in ["Scalar", "PseudoScalar"]:
#		samples["Pbb_{}_{}".format(mass, spin)] = ["Spin0_ggPhibb1j_{}_{}".format(mass, spin)]

# Skims. Dictionary is [sample name]:[path to skim].
skims = {}
skims["JetHTRun2016B"] = [x.strip() for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/files_JetHTRun2016B_PromptReco_v2_resub.txt"))] #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016B_PromptReco_v2_resub.root"]
skims["JetHTRun2016C"] = [x.strip() for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/files_JetHTRun2016C_PromptReco_v2.txt"))] #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016C_PromptReco_v2.root"]
skims["JetHTRun2016D"] = [x.strip() for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/files_JetHTRun2016D_PromptReco_v2.txt"))] #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016D_PromptReco_v2.root"]
skims["JetHTRun2016E"] = [x.strip() for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/files_JetHTRun2016E_PromptReco_v2.txt"))] #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016E_PromptReco_v2.root"]
skims["JetHTRun2016F"] = [x.strip() for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/files_JetHTRun2016F_PromptReco_v1.txt"))] #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016F_PromptReco_v1.root"]
skims["JetHTRun2016G"] = [x.strip() for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/files_JetHTRun2016G_PromptReco_v1.txt"))] #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016G_PromptReco_v1.root"]
skims["JetHTRun2016H"] = [x.strip() for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/files_JetHTRun2016H_PromptReco_v2.txt"))] #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016H_PromptReco_v2.root"]
skims["QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = [x.strip() for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/files_QCD_HT100to200_13TeV.txt"), "r")]
skims["QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = [x.strip() for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/files_QCD_HT200to300_13TeV_ext.txt"), "r")]
skims["QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = [x.strip() for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/files_QCD_HT300to500_13TeV_ext.txt"), "r")]
skims["QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = [x.strip() for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/files_QCD_HT500to700_13TeV_ext.txt"), "r")]
skims["QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = [x.strip() for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/files_QCD_HT700to1000_13TeV_ext.txt"), "r")]
skims["QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = [x.strip() for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/files_QCD_HT1000to1500_13TeV_ext.txt"), "r")]
skims["QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = [x.strip() for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/files_QCD_HT1500to2000_13TeV_ext.txt"), "r")]
skims["QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = [x.strip() for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/files_QCD_HT2000toInf_13TeV_ext.txt"), "r")]
skims["ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1"] = ["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/ST_t-channel_antitop_4f_inclusiveDecays_13TeV_powheg.root"]
skims["ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1"] = [ "root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/ST_t-channel_top_4f_inclusiveDecays_13TeV_powheg.root"]
skims["ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1"] = ["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/ST_tW_antitop_5f_inclusiveDecays_13TeV.root"]
skims["ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1"] = ["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/ST_tW_top_5f_inclusiveDecays_13TeV.root"]
skims["WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = ["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.061/WJetsToQQ_HT_600ToInf_13TeV.root"]
skims["WJetsToQQ_HT180_13TeV"] = ["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/WJetsToQQ_HT180_13TeV.root"]
skims["ZJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = ["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.061/ZJetsToQQ_HT600toInf_13TeV_madgraph.root"]
skims["TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = ["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/TTJets_13TeV.root"]
for mass in signal_masses:
	skims["Spin0_ggPhi12j_g1_{}_Scalar".format(mass)] = [x.strip().replace("/eos/", "root://eoscms.cern.ch//eos/") for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/Spin0_ggPhi12j_g1_{}_Scalar_13TeV_madgraphs.txt"))]
Spin0_ggPhi12j_g1_5_Scalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_25_Scalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_50_Scalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_75_Scalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_100_Scalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_125_Scalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_150_Scalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_200_Scalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_250_Scalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_300_Scalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_350_Scalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_400_Scalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_500_Scalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_600_Scalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_800_Scalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_1000_Scalar_13TeV_madgraph.txt

Spin0_ggPhi12j_g1_800_PseudoScalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_75_PseudoScalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_600_PseudoScalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_5_PseudoScalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_50_PseudoScalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_500_PseudoScalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_350_PseudoScalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_300_PseudoScalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_25_PseudoScalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_250_PseudoScalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_200_PseudoScalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_150_PseudoScalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_125_PseudoScalar_13TeV_madgraph.txt
Spin0_ggPhi12j_g1_1000_PseudoScalar_13TeV_madgraph.txt

# Function to infer the sample from a file path... removing for now, because this doesn't work well on the batch system. E.g. if you have subfiles with generic names (e.g. Output_subjob1.root), there is no way to get the sample.
#def get_sample_from_skim(skim):
#	found_sample = ""
#
#	for sample, filelist in skims.iteritems():
#		for filename in filelist:
#			# Match whole path
#			if skim == filename:
#				found_sample = sample
#				break
#
#			# Match using os.path.samefile
#			if os.path.samefile(filename, skim):
#				found_sample = sample
#				break
#
#			# Match skim subjobs, with generic filenames (Output.root_job...)
#			if "Output.root_job" in skim:
#				file_sample_tag = os.path.basename(os.path.dirname(filename)) # Sample tag is the parent folder
#				if file_sample_tag in skim:
#
#			# Match using basename matching
#			if os.path.basename(filename) == os.path.basename(skim):
#				found_sample = sample
#				break
#			# 
#
#		if found_sample != "":
#			break
#
#	# Search using basename matching
#	if found_sample == "":
#		for sample, filelist
#	return found_sample

# Sklims
sklims = {}
sklims["JetHTRun2016B"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016B_23Sep2016_v1.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016B_23Sep2016_v3_0.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016B_23Sep2016_v3_1.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016B_23Sep2016_v3_2.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016B_23Sep2016_v3_3.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016B_23Sep2016_v3_4.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016B_23Sep2016_v3_5.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016B_23Sep2016_v3_6.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016B_23Sep2016_v3_7.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016B_23Sep2016_v3_8.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016B_23Sep2016_v3_9.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016B_23Sep2016_v3_10.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016B_23Sep2016_v3_11.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016B_23Sep2016_v3_12.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016B_23Sep2016_v3_13.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016B_23Sep2016_v3_14.root"]
sklims["JetHTRun2016C"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016C_23Sep2016_v1_v2.root"]
sklims["JetHTRun2016D"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016D_23Sep2016_v1_0.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016D_23Sep2016_v1_1.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016D_23Sep2016_v1_2.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016D_23Sep2016_v1_3.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016D_23Sep2016_v1_4.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016D_23Sep2016_v1_5.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016D_23Sep2016_v1_6.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016D_23Sep2016_v1_7.root"]
sklims["JetHTRun2016E"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016E_23Sep2016_v1_0.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016E_23Sep2016_v1_1.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016E_23Sep2016_v1_2.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016E_23Sep2016_v1_3.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016E_23Sep2016_v1_4.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016E_23Sep2016_v1_5.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016E_23Sep2016_v1_6.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016E_23Sep2016_v1_7.root"]
sklims["JetHTRun2016F"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016F_23Sep2016_v1.root"]
sklims["JetHTRun2016G"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016G_23Sep2016_v1_v2.root"]
sklims["JetHTRun2016H"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016H_PromptReco_v2.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/JetHTRun2016H_PromptReco_v3.root"]
sklims["QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/QCD_HT100to200_13TeV_1000pb_weighted.root"]
sklims["QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/QCD_HT200to300_13TeV_1000pb_weighted.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/QCD_HT200to300_13TeV_ext_1000pb_weighted.root"]
sklims["QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/QCD_HT300to500_13TeV_1000pb_weighted.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/QCD_HT300to500_13TeV_ext_1000pb_weighted.root"]
sklims["QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/QCD_HT500to700_13TeV_ext_1000pb_weighted.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/QCD_HT500to700_13TeV_1000pb_weighted.root"]
sklims["QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/QCD_HT700to1000_13TeV_ext_1000pb_weighted.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/QCD_HT700to1000_13TeV_1000pb_weighted.root"]
sklims["QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/QCD_HT1000to1500_13TeV_ext_1000pb_weighted.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/QCD_HT1000to1500_13TeV_1000pb_weighted.root"]
sklims["QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/QCD_HT1500to2000_13TeV_1000pb_weighted.root","root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/QCD_HT1500to2000_13TeV_ext_1000pb_weighted.root"]
sklims["QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/QCD_HT2000toInf_13TeV_1000pb_weighted.root"]

sklims["ST_t_antitop"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/ST_t_channel_antitop_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV_powhegV2_madspin_1000pb_weighted.root"]
sklims["ST_t_top"] = [ "root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/ST_t_channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV_powhegV2_madspin_1000pb_weighted.root"]
sklims["ST_tW_antitop"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/ST_tW_antitop_5f_inclusiveDecays_13TeV_powheg_pythia8_TuneCUETP8M2T4_1000pb_weighted.root"]
sklims["ST_tW_top"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/ST_tW_top_5f_inclusiveDecays_13TeV_powheg_pythia8_TuneCUETP8M2T4_1000pb_weighted.root"]

sklims["WJetsToQQ"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/WJetsToQQ_HT180_13TeV_1000pb_weighted.root"]
sklims["DYJetsToQQ"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/DYJetsToQQ_HT180_13TeV_1000pb_weighted.root"]
sklims["TTJets"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/TT_powheg_1000pb_weighted.root"]
sklims["WWTo4Q"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/WWTo4Q_13TeV_powheg_1000pb_weighted.root"]
sklims["ZZ"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/ZZ_13TeV_pythia8_1000pb_weighted.root"]
sklims["WZ"] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.03/cvernier/WZ_13TeV_pythia8_1000pb_weighted.root"]
for mass in signal_masses:
	sklims["DMSpin0_ggPhibb1j_{}".format(mass)] = ["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/DMSpin0_ggPhibb1j_{}.root".format(mass)]

# Need to re-make these sklims for v12! The processing barely did any events.
#for mass in signal_masses:
#	for spin in ["Scalar", "PseudoScalar"]:
#		sklims["Spin0_ggPhibb1j_{}_{}".format(mass, spin)] = ["root://cmsxrootd-site.fnal.gov//store/user/lpchbb/zprimebits-v12.02/norm/Spin0_ggPhi12j_g1_{}_{}_13TeV_madgraph_1000pb_weighted.root".format(mass, spin)]


def get_sample_from_sklim(sklim):
	found_sample = ""
	for sample, filename in sklims.iteritems():
		if os.path.basename(filename) == os.path.basename(sklim):
			found_sample = sample
			break
	return found_sample

