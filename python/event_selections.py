import os
import sys
import ROOT
ROOT.gSystem.Load(os.path.expandvars("$CMSSW_BASE/lib/$SCRAM_ARCH/libMyToolsRootUtils.so"))
ROOT.gInterpreter.Declare("#include \"MyTools/AnalysisTools/interface/EventSelector.h\"")
ROOT.gSystem.Load(os.path.expandvars("$CMSSW_BASE/lib/$SCRAM_ARCH/libMyToolsAnalysisTools.so"))
ROOT.gSystem.Load(os.path.expandvars("$CMSSW_BASE/lib/$SCRAM_ARCH/libDAZSLEPhiBBPlusJet.so"))

def MakeSRSelector(jet_type, n2_ddt_cut=0., tau21_ddt_cut=None, jet_systematic="nominal"):
	event_selector = ROOT.EventSelector("BaconData")()
	selector_name = "EventSelector_SR"
	if jet_systematic != "nominal":
		selector_name += "_" + jet_systematic
	ROOT.BaconEventCutFunctions.Configure(event_selector, selector_name)
	cut_parameters = {}
	cut_descriptors = {}

	if jet_type == "AK8":
		cut_parameters["Min_AK8Puppijet0_pt"] = ROOT.vector("double")()
		cut_parameters["Min_AK8Puppijet0_pt"].push_back(450.)
		cut_descriptors["Min_AK8Puppijet0_pt"] = ROOT.vector("TString")()
		cut_descriptors["Min_AK8Puppijet0_pt"].push_back(jet_systematic)
		event_selector.RegisterCut("Min_AK8Puppijet0_pt", cut_descriptors["Min_AK8Puppijet0_pt"], cut_parameters["Min_AK8Puppijet0_pt"])

		cut_parameters["Min_AK8Puppijet0_msd_puppi"] = ROOT.vector("double")()
		cut_parameters["Min_AK8Puppijet0_msd_puppi"].push_back(40.)
		event_selector.RegisterCut("Min_AK8Puppijet0_msd_puppi", ROOT.vector("TString")(), cut_parameters["Min_AK8Puppijet0_msd_puppi"])

		cut_parameters["AK8Puppijet0_isTightVJet"] = ROOT.vector("double")()
		event_selector.RegisterCut("AK8Puppijet0_isTightVJet", ROOT.vector("TString")(), cut_parameters["AK8Puppijet0_isTightVJet"])
	elif jet_type == "CA15":
		cut_parameters["Min_CA15CHSjet0_pt"] = ROOT.vector("double")()
		cut_parameters["Min_CA15CHSjet0_pt"].push_back(450.)
		cut_descriptors["Min_CA15CHSjet0_pt"] = ROOT.vector("TString")()
		cut_descriptors["Min_CA15CHSjet0_pt"].push_back(jet_systematic)
		event_selector.RegisterCut("Min_CA15CHSjet0_pt", cut_descriptors["Min_CA15CHSjet0_pt"], cut_parameters["Min_CA15CHSjet0_pt"])

		cut_parameters["Min_CA15CHSjet0_msd"] = ROOT.vector("double")()
		cut_parameters["Min_CA15CHSjet0_msd"].push_back(40.)
		event_selector.RegisterCut("Min_CA15CHSjet0_msd", ROOT.vector("TString")(), cut_parameters["Min_CA15CHSjet0_msd"])

		cut_parameters["CA15CHSjet0_isTightVJet"] = ROOT.vector("double")()
		event_selector.RegisterCut("CA15CHSjet0_isTightVJet", ROOT.vector("TString")(), cut_parameters["CA15CHSjet0_isTightVJet"])

	cut_parameters["Max_neleLoose"] = ROOT.vector("double")()
	cut_parameters["Max_neleLoose"].push_back(0)
	event_selector.RegisterCut("Max_neleLoose", ROOT.vector("TString")(), cut_parameters["Max_neleLoose"])

	cut_parameters["Max_nmuLoose"] = ROOT.vector("double")()
	cut_parameters["Max_nmuLoose"].push_back(0)
	event_selector.RegisterCut("Max_nmuLoose", ROOT.vector("TString")(), cut_parameters["Max_nmuLoose"])

	cut_parameters["Max_ntau"] = ROOT.vector("double")()
	cut_parameters["Max_ntau"].push_back(0)
	event_selector.RegisterCut("Max_ntau", ROOT.vector("TString")(), cut_parameters["Max_ntau"])

	cut_parameters["Max_puppet"] = ROOT.vector("double")()
	cut_parameters["Max_puppet"].push_back(180.)
	cut_descriptors["Max_puppet"] = ROOT.vector("TString")()
	cut_descriptors["Max_puppet"].push_back(jet_systematic)
	event_selector.RegisterCut("Max_puppet", cut_descriptors["Max_puppet"], cut_parameters["Max_puppet"])

	if jet_type == "CA15":
		print "[setup_limits::start] WARNING : Adding cut on njets near CA15 jet. These are calculated w.r.t. AK8 jet, so might not be consistent!"
	cut_parameters["Max_nAK4PuppijetsPt30dR08_0"] = ROOT.vector("double")()
	cut_parameters["Max_nAK4PuppijetsPt30dR08_0"].push_back(4)
	event_selector.RegisterCut("Max_nAK4PuppijetsPt30dR08_0", ROOT.vector("TString")(), cut_parameters["Max_nAK4PuppijetsPt30dR08_0"])

	# AK8 or CA15 cuts
	if jet_type == "AK8":
		if tau21_ddt_cut != None:
			cut_parameters["Max_AK8Puppijet0_tau21DDT"] = ROOT.vector("double")()
			cut_parameters["Max_AK8Puppijet0_tau21DDT"].push_back(tau21_ddt_cut)
			event_selector.RegisterCut("Max_AK8Puppijet0_tau21DDT", ROOT.vector("TString")(), cut_parameters["Max_AK8Puppijet0_tau21DDT"])
		else:
			cut_parameters["Max_AK8Puppijet0_N2DDT"] = ROOT.vector("double")()
			cut_parameters["Max_AK8Puppijet0_N2DDT"].push_back(n2_ddt_cut)
			event_selector.RegisterCut("Max_AK8Puppijet0_N2DDT", ROOT.vector("TString")(), cut_parameters["Max_AK8Puppijet0_N2DDT"])
	elif jet_type == "CA15":
		pass
		# CA15 jets don't have an N2 branch in latest skims!
		#cut_parameters["Max_CA15CHSjet0_N2DDT"] = ROOT.vector("double")()
		#cut_parameters["Max_CA15CHSjet0_N2DDT"].push_back(n2_ddt_cut)
		#event_selector.RegisterCut("Max_CA15CHSjet0_N2DDT", ROOT.vector("TString")(), cut_parameters["Max_CA15CHSjet0_N2DDT"])

	return event_selector

def MakeMuCRSelector(jet_type, n2_ddt_cut=0., jet_systematic="nominal"):
	event_selector = ROOT.EventSelector("BaconData")()
	selector_name = "EventSelector_muCR"
	if jet_systematic != "nominal":
		selector_name += "_" + jet_systematic
	ROOT.BaconEventCutFunctions.Configure(event_selector, selector_name)
	cut_parameters = {}
	cut_descriptors = {}

	if jet_type == "AK8":
		cut_parameters["Min_AK8Puppijet0_pt"] = ROOT.vector("double")()
		cut_parameters["Min_AK8Puppijet0_pt"].push_back(400.)
		cut_descriptors["Min_AK8Puppijet0_pt"] = ROOT.vector("TString")()
		cut_descriptors["Min_AK8Puppijet0_pt"].push_back(jet_systematic)
		event_selector.RegisterCut("Min_AK8Puppijet0_pt", cut_descriptors["Min_AK8Puppijet0_pt"], cut_parameters["Min_AK8Puppijet0_pt"])

		cut_parameters["Min_AK8Puppijet0_msd_puppi"] = ROOT.vector("double")()
		cut_parameters["Min_AK8Puppijet0_msd_puppi"].push_back(40.)
		event_selector.RegisterCut("Min_AK8Puppijet0_msd_puppi", ROOT.vector("TString")(), cut_parameters["Min_AK8Puppijet0_msd_puppi"])

		cut_parameters["AK8Puppijet0_isTightVJet"] = ROOT.vector("double")()
		event_selector.RegisterCut("AK8Puppijet0_isTightVJet", ROOT.vector("TString")(), cut_parameters["AK8Puppijet0_isTightVJet"])
	elif jet_type == "CA15":
		cut_parameters["Min_CA15CHSjet0_pt"] = ROOT.vector("double")()
		cut_parameters["Min_CA15CHSjet0_pt"].push_back(400.)
		cut_descriptors["Min_CA15CHSjet0_pt"] = ROOT.vector("TString")()
		cut_descriptors["Min_CA15CHSjet0_pt"].push_back(jet_systematic)
		event_selector.RegisterCut("Min_CA15CHSjet0_pt", cut_descriptors["Min_CA15CHSjet0_pt"], cut_parameters["Min_CA15CHSjet0_pt"])

		cut_parameters["Min_CA15CHSjet0_msd"] = ROOT.vector("double")()
		cut_parameters["Min_CA15CHSjet0_msd"].push_back(40.)
		event_selector.RegisterCut("Min_CA15CHSjet0_msd", ROOT.vector("TString")(), cut_parameters["Min_CA15CHSjet0_msd"])

		cut_parameters["CA15CHSjet0_isTightVJet"] = ROOT.vector("double")()
		event_selector.RegisterCut("CA15CHSjet0_isTightVJet", ROOT.vector("TString")(), cut_parameters["CA15CHSjet0_isTightVJet"])

	# General event cuts, independent of jet type
	cut_parameters["Max_neleLoose"] = ROOT.vector("double")()
	cut_parameters["Max_neleLoose"].push_back(0)
	event_selector.RegisterCut("Max_neleLoose", ROOT.vector("TString")(), cut_parameters["Max_neleLoose"])

	cut_parameters["Max_ntau"] = ROOT.vector("double")()
	cut_parameters["Max_ntau"].push_back(0)
	event_selector.RegisterCut("Max_ntau", ROOT.vector("TString")(), cut_parameters["Max_ntau"])

	cut_parameters["Min_nmuLoose"] = ROOT.vector("double")()
	cut_parameters["Min_nmuLoose"].push_back(1)
	event_selector.RegisterCut("Min_nmuLoose", ROOT.vector("TString")(), cut_parameters["Min_nmuLoose"])

	cut_parameters["Max_nmuLoose"] = ROOT.vector("double")()
	cut_parameters["Max_nmuLoose"].push_back(1)
	event_selector.RegisterCut("Max_nmuLoose", ROOT.vector("TString")(), cut_parameters["Max_nmuLoose"])

	cut_parameters["Min_vmuoLoose0_pt"] = ROOT.vector("double")()
	cut_parameters["Min_vmuoLoose0_pt"].push_back(55.)
	event_selector.RegisterCut("Min_vmuoLoose0_pt", ROOT.vector("TString")(), cut_parameters["Min_vmuoLoose0_pt"])

	cut_parameters["Max_vmuoLoose0_abseta"] = ROOT.vector("double")()
	cut_parameters["Max_vmuoLoose0_abseta"].push_back(2.1)
	event_selector.RegisterCut("Max_vmuoLoose0_abseta", ROOT.vector("TString")(), cut_parameters["Max_vmuoLoose0_abseta"])

	cut_parameters["Min_dphi_mu_jet"] = ROOT.vector("double")()
	cut_parameters["Min_dphi_mu_jet"].push_back(2. * ROOT.TMath.Pi() / 3.)
	cut_descriptors["Min_dphi_mu_jet"] = ROOT.vector("TString")()
	cut_descriptors["Min_dphi_mu_jet"].push_back(jet_type)
	event_selector.RegisterCut("Min_dphi_mu_jet", cut_descriptors["Min_dphi_mu_jet"], cut_parameters["Min_dphi_mu_jet"])

	cut_parameters["Min_nAK4PuppijetsMPt50dR08_0"] = ROOT.vector("double")()
	cut_parameters["Min_nAK4PuppijetsMPt50dR08_0"].push_back(1.)
	event_selector.RegisterCut("Min_nAK4PuppijetsMPt50dR08_0", ROOT.vector("TString")(), cut_parameters["Min_nAK4PuppijetsMPt50dR08_0"])

	# AK8 or CA15 cuts
	if jet_type == "AK8":
		cut_parameters["Max_AK8Puppijet0_N2DDT"] = ROOT.vector("double")()
		cut_parameters["Max_AK8Puppijet0_N2DDT"].push_back(n2_ddt_cut)
		event_selector.RegisterCut("Max_AK8Puppijet0_N2DDT", ROOT.vector("TString")(), cut_parameters["Max_AK8Puppijet0_N2DDT"])

		cut_parameters["AK8Puppijet0_isTightVJet"] = ROOT.vector("double")()
		event_selector.RegisterCut("AK8Puppijet0_isTightVJet", ROOT.vector("TString")(), cut_parameters["AK8Puppijet0_isTightVJet"])

	elif jet_type == "CA15":
		cut_parameters["Max_CA15CHSjet0_N2DDT"] = ROOT.vector("double")()
		cut_parameters["Max_CA15CHSjet0_N2DDT"].push_back(n2_ddt_cut)
		event_selector.RegisterCut("Max_CA15CHSjet0_N2DDT", ROOT.vector("TString")(), cut_parameters["Max_CA15CHSjet0_N2DDT"])

		cut_parameters["CA15CHSjet0_isTightVJet"] = ROOT.vector("double")()
		event_selector.RegisterCut("CA15CHSjet0_isTightVJet", ROOT.vector("TString")(), cut_parameters["CA15CHSjet0_isTightVJet"])
	return event_selector