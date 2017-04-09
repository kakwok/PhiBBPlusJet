import os
import sys
import ROOT
from DAZSLE.PhiBBPlusJet.analysis_base import AnalysisBase
import DAZSLE.PhiBBPlusJet.analysis_configuration as config
from DAZSLE.PhiBBPlusJet.bacon_event_selector import *
from math import ceil, sqrt,floor
import array
import time

import ROOT
from ROOT import *
gInterpreter.Declare("#include \"MyTools/RootUtils/interface/SeabornInterface.h\"")
gInterpreter.Declare("#include \"MyTools/RootUtils/interface/HistogramManager.h\"")
gSystem.Load(os.path.expandvars("$CMSSW_BASE/lib/$SCRAM_ARCH/libMyToolsRootUtils.so"))
gInterpreter.Declare("#include \"MyTools/AnalysisTools/interface/EventSelector.h\"")
gSystem.Load(os.path.expandvars("$CMSSW_BASE/lib/$SCRAM_ARCH/libMyToolsAnalysisTools.so"))
gSystem.Load(os.path.expandvars("$CMSSW_BASE/lib/$SCRAM_ARCH/libDAZSLEPhiBBPlusJet.so"))
#from ROOT import gInterpreter, gSystem, gROOT, gStyle, Root, TCanvas, TLegend, TH1F, TFile, TGraphErrors
gROOT.SetBatch(ROOT.kTRUE);
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
seaborn = Root.SeabornInterface()
seaborn.Initialize()

class TestPyEventSelector(AnalysisBase):
	def __init__(self, sample_name, tree_name="otree"):
		super(TestPyEventSelector, self).__init__(tree_name=tree_name)
		self._output_path = ""
		self._input_nevents = 0
		self._jet_type = "AK8"

	# Overload add_file to extract the number of input events to the skims, stored in histogram NEvents in the same file as the trees
	def add_file(self, filename):
		super(TestPyEventSelector, self).add_file(filename)
		f = ROOT.TFile.Open(filename, "READ")
		self._input_nevents += f.Get("NEvents").Integral()
		f.Close()

	def set_output_path(self, output_path):
		self._output_path = output_path
		os.system("mkdir -pv {}".format(os.path.dirname(self._output_path)))

	def start(self):
		self._processed_events = 0

		# Histograms
		self._pt_bins = array.array("d", [450., 500.,550.,600.,675.,800.,1000.])

		self._histograms = ROOT.Root.HistogramManager()
		self._histograms.AddPrefix("h_")

		self._histograms.AddTH1F("input_nevents", "input_nevents", "", 1, -0.5, 0.5)
		self._histograms.GetTH1F("input_nevents").SetBinContent(1, self._input_nevents)
		self._histograms.AddTH1D("processed_nevents", "processed_nevents", "", 1, -0.5, 0.5)

		self._histograms.AddTH1D("pass_nevents", "pass_nevents", "", 1, -0.5, 0.5)
		self._histograms.AddTH1D("pass_nevents_weighted", "pass_nevents_weighted", "", 1, -0.5, 0.5)
		self._histograms.AddTH2D("pt_dcsv", "pt_dcsv", "p_{T} [GeV]", 200, 0., 2000., "Double b-tag", 20, -1., 1.)
		self._histograms.AddTH2D("pass", "; {} m_{{SD}}^{{PUPPI}} (GeV); {} p_{{T}} (GeV)".format(self._jet_type, self._jet_type), "m_{SD}^{PUPPI} [GeV]", 70, 40, 600, "p_{T} [GeV]", len(self._pt_bins) - 1, self._pt_bins)
		self._histograms.AddTH2D("pass_unweighted", "; {} m_{{SD}}^{{PUPPI}} (GeV); {} p_{{T}} (GeV)".format(self._jet_type, self._jet_type), "m_{SD}^{PUPPI} [GeV]", 70, 40, 600, "p_{T} [GeV]", len(self._pt_bins) - 1, self._pt_bins)
		self._histograms.AddTH2D("fail", "; {} m_{{SD}}^{{PUPPI}} (GeV); {} p_{{T}} (GeV)".format(self._jet_type, self._jet_type), "m_{SD}^{PUPPI} [GeV]", 70, 40, 600, "p_{T} [GeV]", len(self._pt_bins) - 1, self._pt_bins)
		self._histograms.AddTH2D("fail_unweighted", "; {} m_{{SD}}^{{PUPPI}} (GeV); {} p_{{T}} (GeV)".format(self._jet_type, self._jet_type), "m_{SD}^{PUPPI} [GeV]", 70, 40, 600, "p_{T} [GeV]", len(self._pt_bins) - 1, self._pt_bins)


		# Event selections
		self._event_selector = BaconEventSelector()
		self._event_selector.add_cut("Min_AK8Puppijet0_msd", 40.)
		self._event_selector.add_cut("Min_AK8Puppijet0_pt", {"Min_AK8Puppijet0_pt":450., "systematic":"nominal"})
		self._event_selector.add_cut("AK8Puppijet0_isTightVJet", None)
		self._event_selector.add_cut("Max_neleLoose", 0)
		self._event_selector.add_cut("Max_nmuLoose", 0)
		self._event_selector.add_cut("Max_ntau", 0)
		self._event_selector.add_cut("Max_puppet", {"Max_puppet":180., "systematic":"nominal"})
		self._event_selector.add_cut("Max_nAK4PuppijetsPt30dR08_0", 4)
		self._event_selector.add_cut("Max_AK8Puppijet0_tau21DDT", 0.55)

	def run(self, max_nevents=-1, first_event=0):
		if max_nevents > 0:
			limit_nevents = min(max_nevents, self._chain.GetEntries())
		else:
			limit_nevents = self._chain.GetEntries()

		n_checkpoints = 20
		print_every = int(ceil(1. * limit_nevents / n_checkpoints))

		print "[TestPyEventSelector::run] INFO : Running loop over tree from event {} to {}".format(first_event, limit_nevents - 1)

		self.start_timer()
		for entry in xrange(first_event, limit_nevents):
			self.print_progress(entry, first_event, limit_nevents, print_every)
			self._histograms.GetTH1D("processed_nevents").Fill(0)
			self._processed_events += 1
			self._data.GetEntry(entry)

			self._event_selector.process_event(self._data, 1.)
			if self._event_selector.event_pass():
				self._histograms.GetTH1D("pass_nevents").Fill(0)
				self._histograms.GetTH1D("pass_nevents_weighted").Fill(0, 1.)

				fatjet_pt = self._data.AK8Puppijet0_pt
				fatjet_msd = self._data.AK8Puppijet0_msd_puppi
				fatjet_dcsv = self._data.AK8CHSjet0_doublecsv
				self._histograms.GetTH2D("pt_dcsv").Fill(fatjet_pt, fatjet_dcsv, 1.)

				if fatjet_dcsv > 0.9:
					self._histograms.GetTH2D("pass").Fill(fatjet_msd, fatjet_pt, 1.)
					self._histograms.GetTH2D("pass_unweighted").Fill(fatjet_msd, fatjet_pt)
				else:
					self._histograms.GetTH2D("fail").Fill(fatjet_msd, fatjet_pt, 1.)
					self._histograms.GetTH2D("fail_unweighted").Fill(fatjet_msd, fatjet_pt)
	def finish(self):
		if self._output_path == "":
			self._output_path = "/uscms/home/dryu/DAZSLE/data/LimitSetting/TestPyEventSelector.root".format(time.time)
			print "[SignalCutflow::finish] WARNING : Output path was not provided! Saving to {}".format(self._output_path)
		print "[SignalCutflow::finish] INFO : Saving histograms to {}".format(self._output_path)
		f_out = ROOT.TFile(self._output_path, "RECREATE")
		self._histograms.SaveAll(f_out)
		self._event_selector.print_cutflow()
		self._event_selector.make_cutflow_histograms(f_out)
		self._event_selector.save_nminusone_histograms(f_out)
		f_out.Close()

if __name__ == "__main__":
	samples = ["DMSbb100"]
	sample_files = {}
	sample_files["DMSbb100"] = ["/eos/uscms//store/user/jduarte1/zprimebits-v11.062/DMSpin0_ggPhibb1j_100/Output.root_job0_file0.root"]

	for sample in samples:
		print "\n *** Running sample {}".format(sample)
		if "DMSbb" in sample or args.skim_inputs:
			tree_name = "Events"
		else:
			tree_name = "otree"

		# Sanity check: make sure tree exists in file
		for filename in sample_files[sample]:
			print "Checking " + filename
			f = TFile(filename, "READ")
			t = f.Get(tree_name)
			if not t:
				if tree_name == "otree":
					backup_tree_name = "Events"
				else:
					backup_tree_name = "otree"
				t_backup = f.Get(backup_tree_name)
				if t_backup:
					print "[setup_limits] WARNING : Didn't find tree {} in input file, but did find {}. Changing the tree name, but try to fix this.".format(tree_name, backup_tree_name)
					tree_name = backup_tree_name
				else:
					print "[setup_limits] ERROR : Didn't find tree {} in input file, nor {}. Quitting!".format(tree_name, backup_tree_name)
					sys.exit(1)
		tester = TestPyEventSelector(sample, tree_name=tree_name)
		for filename in sample_files[sample]:
			print "Input file {}".format(filename)
			tester.add_file(filename)
		tester.start()
		tester.run()
		tester.finish()
