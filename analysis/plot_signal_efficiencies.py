import os
import sys
from ROOT import *
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gInterpreter.Declare("#include \"MyTools/RootUtils/interface/CanvasHelpers.h\"")
gInterpreter.Declare("#include \"MyTools/RootUtils/interface/SeabornInterface.h\"")
gSystem.Load("~/DAZSLE/CMSSW_7_4_7/lib/slc6_amd64_gcc491/libMyToolsRootUtils.so")
seaborn = Root.SeabornInterface()
seaborn.Initialize()
Root.SetCanvasStyle()
gSystem.Load("~/DAZSLE/CMSSW_7_4_7/lib/slc6_amd64_gcc491/libDAZSLEPhiBBPlusJet.so")
import DAZSLE.PhiBBPlusJet.analysis_configuration as config
from DAZSLE.PhiBBPlusJet.signal_efficiency import signal_efficiencies
from DAZSLE.PhiBBPlusJet.signal_efficiency import signal_efficiencies_opt
gStyle.SetPalette(1)
gStyle.SetPaintTextFormat("1.3f")


def PlotOptimizationEfficiencies(jet_type):
	tau21_values = [0.4, 0.45, 0.5, 0.525, 0.55, 0.575, 0.6, 0.65, 0.7]
	dcsv_values = [0.7, 0.75, 0.8, 0.85, 0.875, 0.9, 0.925, 0.95, 0.975]
	for signal in config.simulated_signal_names:
		signal_mass = config.signal_masses[signal]
		if "PSbb" in signal:
			model = "PSbb"
		else:
			model = "Sbb"
		h = TH2D("h_{}".format(signal), "h_{}".format(signal), len(tau21_values), -0.5, len(tau21_values) - 0.5, len(dcsv_values), -0.5, len(dcsv_values) - 0.5)
		for xval, tau21_value in enumerate(tau21_values):
			xbin = xval + 1
			h.GetXaxis().SetBinLabel(xbin, str(tau21_value))
			for yval, dcsv_value in enumerate(dcsv_values):
				ybin = yval + 1
				h.GetYaxis().SetBinLabel(ybin, str(dcsv_value))
				h.SetBinContent(xbin, ybin, signal_efficiencies_opt[tau21_value][dcsv_value][jet_type][model][signal_mass])
		c = TCanvas("c_opt_signal_eff_{}_{}".format(signal, jet_type), "c_opt_signal_eff_{}_{}".format(signal, jet_type), 800, 600)
		c.SetRightMargin(0.2)
		h.GetXaxis().SetTitle("#tau_{21}^{DDT}")
		h.GetYaxis().SetTitle("Double CSV")
		h.GetZaxis().SetTitle("Signal Efficiency")
		h.Draw("colz text")
		c.SaveAs("/uscms/home/dryu/DAZSLE/data/LimitSetting/figures/Optimization/{}.pdf".format(c.GetName()))

def PlotEfficiencyVsMass(model, jet_type):
	tg_eff = TGraph(len(config.signal_model_masses))
	for i, mass in enumerate(config.signal_model_masses):
		tg_eff.SetPoint(i, mass, signal_efficiencies[jet_type][model][mass])
	c = TCanvas("c_signal_eff_{}_{}".format(model, jet_type))
	tg_eff.GetXaxis().SetTitle(model + " mass [GeV]")
	tg_eff.GetYaxis().SetTitle("Selection Efficiency")
	tg_eff.SetMarkerStyle(20)
	tg_eff.SetMarkerSize(1)
	tg_eff.SetLineWidth(2)
	tg_eff.Draw("apl")
	c.SaveAs("/uscms/home/dryu/DAZSLE/data/LimitSetting/figures/{}.pdf".format(c.GetName()))

PlotOptimizationEfficiencies("AK8")
PlotOptimizationEfficiencies("CA15")
PlotEfficiencyVsMass("Sbb", "AK8")
PlotEfficiencyVsMass("PSbb", "AK8")
PlotEfficiencyVsMass("Sbb", "CA15")
PlotEfficiencyVsMass("PSbb", "CA15")


