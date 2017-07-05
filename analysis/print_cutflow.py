import os
import sys
from array import array
import ROOT
from ROOT import *
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gInterpreter.Declare("#include \"MyTools/RootUtils/interface/CanvasHelpers.h\"")
gInterpreter.Declare("#include \"MyTools/RootUtils/interface/SeabornInterface.h\"")
gSystem.Load(os.path.expandvars("$CMSSW_BASE/lib/slc6_amd64_gcc491/libDAZSLEPhiBBPlusJet.so"))
gSystem.Load(os.path.expandvars("$CMSSW_BASE/lib/slc6_amd64_gcc491/libMyToolsRootUtils.so"))
import DAZSLE.PhiBBPlusJet.analysis_configuration as config
import DAZSLE.PhiBBPlusJet.style as style
seaborn = Root.SeabornInterface()
seaborn.Initialize()

formatted_samples = {}
formatted_labels = {}

# Convert a cutflow histogram to a latex table row
def cutflow_histogram_to_row(name, hist):
	if name in formatted_samples:
		row_string = "\t\t" + formatted_samples[name]
	else:
		row_string = "\t\t" + name
	for bin in xrange(1, hist.GetNbinsX() + 1):
		if not hist.GetXaxis().GetBinLabel(bin).EqualTo(""):
			row_string += "\t&\t" + str(hist.GetBinContent(bin))
	row_string += "\t\\\\"
	return row_string

def get_cutflow_headers(hist):
	header_string = "\t\t Sample"
	columns = 1
	for bin in xrange(1, hist.GetNbinsX() + 1):
		if not hist.GetXaxis().GetBinLabel(bin).EqualTo(""):
			raw_label = hist.GetXaxis().GetBinLabel(bin)
			if raw_label in formatted_labels:
				header_string += "\t&\t" + formatted_labels[raw_label]
			else:
				header_string += "\t&\t" + raw_label
			columns += 1
	return header_string, columns

if __name__ == "__main__":
	jet_types = ["AK8", "CA15"]
	regions = ["SR", "muCR"]
	samples = {
		"SR":["data_obs", "Sbb100", "Sbb200", "Sbb300", "qcd", "tqq", "zqq", "wqq", "hbb"]
		"muCR":["data_singlemu", "tqq", "qcd", "wlnu", "zll"]
	}
	for jet_type in jet_types:
		for region in regions:
			# Make latex table
			table_file = open("$HOME/DAZSLE/data/EventSelection/cutflows/{}_{}.tex".format(region, jet_type))
			cutflow_histograms = {}
			row_strings = {}
			header_string = None
			columns = 0
			for sample in samples[region]:
				f = TFile(config.get_histogram_file(region, jet_type), "READ")
				cutflow_histograms[sample] = f.Get("h_CutFlowCounter_{}_weighted".format(region))
				cutflow_histograms[sample].SetName("h_CutFlowCounter_{}_{}_{}".format(jet_type, region, sample))
				cutflow_histograms[sample].SetDirectory(0)
				row_strings[sample] = cutflow_histogram_to_row(sample, cutflow_histograms[sample])
				if not header_string:
					header_string, coluns = get_cutflow_headers(cutflow_histograms[sample])
				f.Close()
			table_file.write("\\begin{table}\n")
			table_file.write("\t\\begin{tabular}{|c|" + "c|".join(["" for x in xrange(columns)]) + "\n")
			table_file.write("\t\t\\hline\n")
			table_file.write(header_string + "\n")
			table_file.write("\t\t\\hline\n")
			for sample in samples[region]:
				table_file.write(row_strings[sample] + "\n")
				table_file.write("\t\t\\hline\n")
			table_file.write("\t\\end{tabular}\n")
			table_file.write("\\end{table}\n")
			table_file.Close()

			# Make pretty plot
			cutflow_canvas = 
