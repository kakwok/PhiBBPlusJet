import os
import sys
import ROOT
from DAZSLE.PhiBBPlusJet.analysis_base import AnalysisBase
import DAZSLE.PhiBBPlusJet.analysis_configuration as config
import DAZSLE.PhiBBPlusJet.event_selections as event_selections
from DAZSLE.PhiBBPlusJet.bacon_event_selector import *
from math import ceil, sqrt,floor
import array

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

class SignalValidation(AnalysisBase):
	def __init__(self, sample_name, tree_name="otree"):
		super(SignalValidation, self).__init__(tree_name=tree_name)
		self._output_path = ""
		self._sample_name = sample_name
		self._input_nevents = 0

	# Overload add_file to extract the number of input events to the skims, stored in histogram NEvents in the same file as the trees
	def add_file(self, filename):
		super(SignalValidation, self).add_file(filename)
		f = ROOT.TFile.Open(filename, "READ")
		if f.Get("NEvents").Integral() == 0:
			print "[SignalValidation::add_file] ERROR : NEvents.Integral() == 0 for file " + filename
			sys.exit(1)
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
		self._histograms.AddTH1D("genVPt", "genVPt", "p_{T} [GeV]", 2000, 0., 2000.)
		self._histograms.AddTH1D("genVEta", "genVEta", "#eta", 100, -5., 5.)
		self._histograms.AddTH1D("genVPhi", "genVPhi", "#phi", 60, -2.*TMath.Pi(), 2.*TMath.Pi())
		self._histograms.AddTH1D("genVMass", "genVMass", "m_{X} [GeV}", 500, 0., 500.)


	def run(self, max_nevents=-1, first_event=0):
		if max_nevents > 0:
			limit_nevents = min(max_nevents, self._chain.GetEntries())
		else:
			limit_nevents = self._chain.GetEntries()

		n_checkpoints = 20
		print_every = int(ceil(1. * limit_nevents / n_checkpoints))

		print "[SignalValidation::run] INFO : Running loop over tree from event {} to {}".format(first_event, limit_nevents - 1)

		self.start_timer()
		for entry in xrange(first_event, limit_nevents):
			self.print_progress(entry, first_event, limit_nevents, print_every)
			self._histograms.GetTH1D("processed_nevents").Fill(0)
			self._processed_events += 1
			self._data.GetEntry(entry)

			self._histograms.GetTH1D("genVPt").Fill(self._data.genVPt)
			self._histograms.GetTH1D("genVEta").Fill(self._data.genVEta)
			self._histograms.GetTH1D("genVPhi").Fill(self._data.genVPhi)
			self._histograms.GetTH1D("genVMass").Fill(self._data.genVMass)


	def finish(self):
		if self._output_path == "":
			self._output_path = os.path.expandvars("$HOME/DAZSLE/data/Validation/SignalValidation_{}.root".format(time.time))
			print "[SignalCutflow::finish] WARNING : Output path was not provided! Saving to {}".format(self._output_path)
		print "[SignalCutflow::finish] INFO : Saving histograms to {}".format(self._output_path)
		f_out = ROOT.TFile(self._output_path, "RECREATE")
		self._histograms.SaveAll(f_out)
		f_out.Close()

# Not using this right now! It was intended for joblib parallel processing, but you weren't able to figure out joblib on condor. 
#def RunSingleFile(args, samples, filename, label="", tree_name="Events"):
#	print "Input file {}".format(filename)
#	signal_validation_histogrammer = SignalValidation(label, tree_name=tree_name)
#	if args.output_folder:
#		signal_validation_histogrammer.set_output_path("{}/InputHistograms_{}.root".format(args.output_folder, label))
#	else:
#		signal_validation_histogrammer.set_output_path("/uscms/home/dryu/DAZSLE/data/Validation/InputHistograms_{}.root".format(label))
#	signal_validation_histogrammer.add_file(filename)
#	signal_validation_histogrammer.start()
#	signal_validation_histogrammer.run()
#	signal_validation_histogrammer.finish()

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='Produce and plot ieta-iphi histograms to look for buggy events')
	input_group = parser.add_mutually_exclusive_group() 
	input_group.add_argument('--all', action="store_true", help="Run over all signal samples")
	input_group.add_argument('--samples', type=str, help="Sample name(s), comma separated. Must be a key in analysis_configuration.skims.")
	input_group.add_argument('--files', type=str, help="Input file name(s), comma separated")
	parser.add_argument('--n_jobs', type=int, default=4, help="For --run, specify the number of parallel jobs.")
	action_group = parser.add_mutually_exclusive_group() 
	action_group.add_argument('--run', action="store_true", help="Run")
	action_group.add_argument('--condor_run', action="store_true", help="Run on condor")
	action_group.add_argument('--plots', action="store_true", help="Make plots")
	#action_group.add_argument('--rhalphabet', action="store_true", help="Run rhalpabet and create workspaces for combine")
	#action_group.add_argument('--datacards', action="store_true", help="Create datacards for combine")
	parser.add_argument('--output_folder', type=str, help="Output folder")
	parser.add_argument('--label', type=str, help="If running with --files, need to specify a label manually, in lieu of the sample names, for the output file naming.")
	parser.add_argument('--skim_inputs', action='store_true', help="Run over skim inputs")
	args = parser.parse_args()

	if args.run or args.condor_run:
		# Make a list of input samples and files
		samples = []
		sample_files = {} # Dictionary is sample : [list of files in sample]
		if args.all:
			supersamples = config.signal_names
			samples = [] 
			for supersample in supersamples:
				samples.extend(config.samples[supersample])
				for sample in config.samples[supersample]:
					if args.skim_inputs:
						sample_files[sample] = config.skims[sample]
					else:
						sample_files[sample] = config.sklims[sample]
		elif args.samples:
			samples = args.samples.split(",")
			for sample in samples:
				if args.skim_inputs:
					sample_files[sample] = config.skims[sample]
				else:
					sample_files[sample] = config.sklims[sample]
		elif args.files:
			files = args.files.split(",")
			for filename in files:
				if args.label:
					this_sample = args.label
				else:
					this_sample = "UnknownSample"
				if not this_sample in sample_files:
					sample_files[this_sample] = []
				sample_files[this_sample].append(filename)
			samples = sample_files.keys()
		print "List of input samples: ",
		print samples
		print "List of samples and files: ",
		print sample_files
		#print "List of sample => input files:",
		#print sample_files


	if args.run:
		#from joblib import Parallel
		#from joblib import delayed
		for sample in samples:
			print "\n *** Running sample {}".format(sample)
			if "Sbb" in sample or args.skim_inputs:
				tree_name = "Events"
			else:
				tree_name = "otree"

			# Sanity check: make sure tree exists in file
			for filename in sample_files[sample]:
				print "[event_selection_histograms] INFO : Checking contents of file {}".format(filename)
				f = ROOT.TFile.Open(filename, "READ")
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
				# Check that the "NEvents" histogram is present
				h_NEvents = f.Get("NEvents")
				if not h_NEvents:
					if "data" in sample:
						print "[setup_limits] ERROR : NEvents histogram in not in this file! It is probably corrupt. This is data, so this problem is fatal."
						sys.exit(1)
					else:
						print "[setup_limits] WARNING : NEvents histogram in not in this file! It is probably corrupt. This is MC, so I am skipping the file. But, you probably want to remove from the input list."
						sample_files[sample].remove(filename)
				
			signal_validation_histogrammer = SignalValidation(sample, tree_name=tree_name)
			if args.output_folder:
				signal_validation_histogrammer.set_output_path("{}/SignalValidation_{}.root".format(args.output_folder, sample))
			else:
				signal_validation_histogrammer.set_output_path(os.path.expandvars("$HOME/DAZSLE/data/Validation/SignalValidation_{}.root".format(sample)))
			for filename in sample_files[sample]:
				print "Input file {}".format(filename)
				signal_validation_histogrammer.add_file(filename)
			signal_validation_histogrammer.start()
			signal_validation_histogrammer.run()
			signal_validation_histogrammer.finish()
			#subjob_index = 0
			#for subjob_index, filename in enumerate(sample_files[sample]):
			#	RunSingleFile(args, samples, filename, label=sample)
			# joblib doesn't work on condor! Yet.
			#if len(sample_files[sample]) >= 2:
			#	Parallel(n_jobs=4)(
			#		delayed(RunSingleFile)(
			#			args, 
			#			samples, 
			#			sample_files[sample][i], 
			#			label="{}_subjob{}".format(sample, i)
			#		) for i in xrange(len(sample_files[sample]))
			#	)
			#else:
			#	RunSingleFile(args, samples, sample_files[sample][0], label=sample)

	if args.condor_run:
		import time
		hadd_scripts = []
		for sample in samples:
			start_directory = os.getcwd()
			job_tag = "job_{}_{}_{}".format(sample, args.jet_type, int(floor(time.time())))
			submission_directory = os.path.expandvars("$HOME/DAZSLE/data/Validation/condor/{}".format(job_tag))
			os.system("mkdir -pv {}".format(submission_directory))
			os.chdir(submission_directory)

			files_per_job = 1
			if args.skim_inputs:
				if "Spin0" in sample or "Sbb" in sample:
					files_per_job = 3

			csubjob_index = 0
			this_job_input_files = []
			input_files_to_transfer = []
			for file_counter, filename in enumerate(sample_files[sample], start=1):
				print file_counter, filename
				if "root://" in filename:
					this_job_input_files.append(filename)
				else:
					input_files_to_transfer.append(filename)
					this_job_input_files.append(os.path.basename(filename))
				
				if file_counter % files_per_job == 0 or file_counter == len(sample_files[sample]):
					print "\nSubmitting jobs now."
					print "\t input_files_to_transfer = ",
					print input_files_to_transfer
					job_script_path = "{}/run_csubjob{}.sh".format(submission_directory, csubjob_index)
					job_script = open(job_script_path, 'w')
					job_script.write("#!/bin/bash\n")
					job_command = "python $CMSSW_BASE/src/DAZSLE/PhiBBPlusJet/analysis/signal_plots.py --jet_type {} --files {} --label {}_csubjob{} --output_folder . --run ".format(args.jet_type, ",".join(this_job_input_files), sample, csubjob_index)
					if args.skim_inputs or args.all_lxplus:
						job_command += " --skim_inputs "
					if args.do_optimization:
						job_command += " --do_optimization "
					job_command += " 2>&1\n"
					job_script.write(job_command)
					job_script.close()
					submission_command = "csub {} --cmssw --no_retar".format(job_script_path)
					if len(input_files_to_transfer) >= 1:
						submission_command += " -F " + ",".join(input_files_to_transfer)
					print submission_command

					# Save csub command for resubmission attempts
					submission_script_path = "{}/csub_command{}.sh".format(submission_directory, csubjob_index)
					submission_script = open(submission_script_path, "w")
					submission_script.write("#!/bin/bash\n")
					submission_script.write(submission_command + "\n")
					submission_script.close()

					# Submit jobs
					os.system(submission_command)
					this_job_input_files = []
					input_files_to_transfer = []
					csubjob_index += 1
			hadd_scripts.append("{}/hadd.sh".format(submission_directory))
			hadd_script = open("{}/hadd.sh".format(submission_directory), "w")
			hadd_script.write("#!/bin/bash\n")
			hadd_script.write(os.path.expandvars("hadd $HOME/DAZSLE/data/Validation/SignalValidation.root {}/SignalValidation*csubjob*root\n".format(submission_directory)))
			hadd_script.close()
			os.chdir(start_directory)
		# One hadd script to rule them all
		master_hadd_script_path = os.path.expandvars("$HOME/DAZSLE/data/Validation/condor/master_hadd")
		if not args.all:
			master_hadd_script_path += "_" + str(int(floor(time.time())))
		master_hadd_script_path += ".sh"
		master_hadd_script = open(master_hadd_script_path, "w")
		master_hadd_script.write("#!/bin/bash\n")
		for hadd_script_path in hadd_scripts:
			master_hadd_script.write("source " + hadd_script_path + "\n")
		master_hadd_script.close()		

	if args.plots:
		for sample in samples:
			print "\n *** Plotting sample {}".format(sample)
			if args.output_folder:
				histogram_file = TFile("{}/SignalValidation_{}.root".format(args.output_folder, sample), "READ")
			else:
				histogram_file = TFile(os.path.expandvars("$HOME/DAZSLE/data/Validation/SignalValidation_{}.root".format(sample)), "READ")
			for var in ["genVPt", "genVEta", "genVPhi", "genVMass"]:
				c = TCanvas("c_{}_{}".format(sample, var), "c_{}_{}".format(sample, var), 700, 500)
				h = histogram_file.Get("h_{}".format(var))
				h.Draw()
				c.SaveAs("$HOME/DAZSLE/data/Validation/figures/{}.pdf".format(c.GetName()))
			histogram_file.Close()
