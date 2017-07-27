# Get signal acceptance and efficiencies
import os
import sys
import pickle
import time
from ROOT import *
import DAZSLE.PhiBBPlusJet.analysis_configuration as config
from DAZSLE.PhiBBPlusJet.cuts import cuts

signal_efficiencies = pickle.load(open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/PhiBBPlusJet/python/signal_efficiencies.pkl"), "rb"))
signal_efficiencies_opt = pickle.load(open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/PhiBBPlusJet/python/signal_efficiencies_opt.pkl"), "rb"))

if __name__ == "__main__":
	timestamp = str(time.time()).replace(".","_")
	# Get the signal efficiencies from cutflow histograms and print
	jet_types = ["AK8", "CA15"]
	models = ["Sbb", "PSbb"]
	masses = {"Sbb":config.signal_model_masses, "PSbb":config.signal_model_masses}

	this_signal_efficiencies = {}
	this_signal_efficiencies_opt = {}

	for jet_type in jet_types:
		this_signal_efficiencies[jet_type] = {}
		for model in models:
			this_signal_efficiencies[jet_type][model] = {}
			for mass in masses[model]:
				histogram_file = TFile("~/DAZSLE/data/LimitSetting/InputHistograms_{}{}_{}.root".format(model, mass, jet_type), "READ")
				cutflow_histogram = histogram_file.Get("CutFlowCounter_EventSelector_SR_weighted")
				inclusive = cutflow_histogram.GetBinContent(1)
				pass_histogram = histogram_file.Get("h_SR_{}_pass".format(jet_type))
				if not pass_histogram:
					print "ERROR : Couldn't get histogram {} from file {}".format("h_SR_{}_pass".format(jet_type), histogram_file.GetPath())
					sys.exit(1)
				xbin_min = pass_histogram.GetXaxis().FindBin(cuts[jet_type]["MSD"][0]+1.e-5)
				xbin_max = pass_histogram.GetXaxis().FindBin(cuts[jet_type]["MSD"][1]-1.e-5)
				ybin_min = pass_histogram.GetYaxis().FindBin(cuts[jet_type]["PT"][0]+1.e-5)
				ybin_max = pass_histogram.GetYaxis().FindBin(cuts[jet_type]["PT"][1]-1.e-5)
				final = pass_histogram.Integral(xbin_min, xbin_max, ybin_min, ybin_max)
				this_signal_efficiencies[jet_type][model][mass] = float(final)/float(inclusive)
	pickle.dump(this_signal_efficiencies, open("signal_efficiencies.pkl.{}".format(timestamp), "wb"))
	# tau21 optimization
	tau21_values = [0.4, 0.45, 0.5, 0.525, 0.55, 0.575, 0.6, 0.65, 0.7]
	dcsv_values = [0.7, 0.75, 0.8, 0.85, 0.875, 0.9, 0.925, 0.95, 0.975]

	for tau21_value in tau21_values:
		this_signal_efficiencies_opt[tau21_value] = {}
		for dcsv_value in dcsv_values:
			this_signal_efficiencies_opt[tau21_value][dcsv_value] = {}
			for jet_type in jet_types:
				this_signal_efficiencies_opt[tau21_value][dcsv_value][jet_type] = {}
				for model in models:
					this_signal_efficiencies_opt[tau21_value][dcsv_value][jet_type][model] = {}
					for mass in masses[model]:
						histogram_file = TFile("~/DAZSLE/data/LimitSetting/InputHistograms_{}{}_{}.root".format(model, mass, jet_type), "READ")
						cutflow_histogram = histogram_file.Get("CutFlowCounter_EventSelector_SR_tau21ddt{}_weighted".format(tau21_value))
						inclusive = cutflow_histogram.GetBinContent(1)
						pass_histogram = histogram_file.Get("h_SR_tau21ddt{}_{}_pass_dcsv{}".format(tau21_value, jet_type, dcsv_value))
						if not pass_histogram:
							print "ERROR : Couldn't get histogram {} from file {}".format("h_SR_tau21ddt{}_{}_pass_dcsv{}".format(tau21_value, jet_type, dcsv_value), histogram_file.GetPath())
							sys.exit(1)

						final = pass_histogram.Integral()
						this_signal_efficiencies_opt[tau21_value][dcsv_value][jet_type][model][mass] = float(final)/float(inclusive)
	pickle.dump(this_signal_efficiencies_opt, open("signal_efficiencies_opt.pkl.{}".format(timestamp), "wb"))

	print this_signal_efficiencies
	print this_signal_efficiencies_opt
	print "To use these values, execute the following:"
	print "mv signal_efficiencies.pkl.{}".format(timestamp) + " signal_efficiencies.pkl"
	print "mv signal_efficiencies_opt.pkl.{}".format(timestamp) + " signal_efficiencies_opt.pkl"
