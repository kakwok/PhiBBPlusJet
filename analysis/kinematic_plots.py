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


def DataMCPlot(var, selection, jet_type, data_name="data_obs", signal_names=["Sbb100"], backgrounds=["qcd","tqq","wqq","zqq","hbb","stqq","vvqq"], logy=False, rebin=None, legend_position="right", x_range=None):
	print "Welcome to DataMCPlot({}, {}, {}, {})".format(var, selection, jet_type, data_name)
	for what in ["pass", "fail", "inclusive"]:
		print "Input file: " + config.get_histogram_file(selection, jet_type)
		histogram_file = TFile(config.get_histogram_file(selection, jet_type), "READ")
		background_histograms = {}
		total_bkgd_histogram = None
		first = True
		for background in backgrounds:
			if var == "msd":
				if what == "pass":
					hname = "{}_pass".format(background)
					background_histograms[background] = histogram_file.Get(hname).ProjectionX()
				elif what == "fail":
					hname = "{}_fail".format(background)
					background_histograms[background] = histogram_file.Get(hname).ProjectionX()
				else:
					hname1 = "{}_pass".format(background)
					background_histograms[background] = histogram_file.Get(hname1).ProjectionX()
					hname2 = "{}_fail".format(background)
					background_histograms[background].Add(histogram_file.Get(hname2).ProjectionX())
			else:
				hname = "{}_{}".format(background, var)
				if what == "pass":
					hname += "_pass"
				elif what == "fail":
					hname += "_fail"
				background_histograms[background] = histogram_file.Get(hname)
			if not background_histograms[background]:
				print "[DataMCPlot] ERROR : Couldn't find histogram {} in file {}".format(hname, histogram_file.GetPath())
			background_histograms[background].SetDirectory(0)
			background_histograms[background].SetFillColor(style.background_colors[background])
			if first:
				first = False
				total_bkgd_histogram = background_histograms[background].Clone()
				total_bkgd_histogram.SetDirectory(0)
			else:
				total_bkgd_histogram.Add(background_histograms[background])

		# Data histogram
		if var == "msd":
			if what == "pass":
				hname = "{}_pass".format(data_name)
				data_histogram = histogram_file.Get(hname).ProjectionX()
			elif what == "fail":
				hname = "{}_fail".format(data_name)
				data_histogram = histogram_file.Get(hname).ProjectionX()
			else:
				hname1 = "{}_pass".format(data_name)
				data_histogram = histogram_file.Get(hname1).ProjectionX()
				hname2 = "{}_fail".format(data_name)
				data_histogram.Add(histogram_file.Get(hname2).ProjectionX())
		else:
			hname = "{}_{}".format(data_name, var)
			if what == "pass":
				hname += "_pass"
			elif what == "fail":
				hname += "_fail"
			data_histogram = histogram_file.Get(hname)
		data_histogram.SetDirectory(0)

		# Signal histograms
		signal_histograms = {}
		for signal_name in signal_names:
			if var == "msd":
				if what == "pass":
					hname = "{}_pass".format(signal_name)
					signal_histograms[signal_name] = histogram_file.Get(hname).ProjectionX()
				elif what == "fail":
					hname = "{}_fail".format(signal_name)
					signal_histograms[signal_name] = histogram_file.Get(hname).ProjectionX()
				else:
					hname1 = "{}_pass".format(signal_name)
					signal_histograms[signal_name] = histogram_file.Get(hname1).ProjectionX()
					hname2 = "{}_fail".format(signal_name)
					signal_histograms[signal_name].Add(histogram_file.Get(hname2).ProjectionX())
			else:
				hname = "{}_{}".format(signal_name, var)
				if what == "pass":
					hname += "_pass"
				elif what == "fail":
					hname += "_fail"
				signal_histograms[signal_name] = histogram_file.Get(hname)
			signal_histograms[signal_name].SetDirectory(0)

		if rebin:
			for background_name, background_histogram in background_histograms.iteritems():
				background_histogram.Rebin(rebin)
			total_bkgd_histogram.Rebin(rebin)
			data_histogram.Rebin(rebin)
			for signal_name, signal_histogram in signal_histograms.iteritems():
				signal_histogram.Rebin(rebin)

		# Sort backgrounds by integral, and make THStack (and legend)
		if legend_position == "right":
			l = TLegend(0.6, 0.4, 0.88, 0.88)
		elif legend_position == "left":
			l = TLegend(0.2, 0.4, 0.48, 0.88)
		l.SetFillColor(0)
		l.SetBorderSize(0)
		l.AddEntry(data_histogram, "Data 2016", "p")
		l.AddEntry(total_bkgd_histogram, "Total background", "l")
		bkgds_sorted = backgrounds
		bkgds_sorted.sort(key=lambda x: background_histograms[x].Integral())
		bkgd_stack = THStack("bkgd_stack", "bkgd_stack")
		for bkgd in bkgds_sorted:
			bkgd_stack.Add(background_histograms[bkgd])
		for bkgd in reversed(bkgds_sorted):
			l.AddEntry(background_histograms[bkgd], bkgd, "f")
		for signal_name in signal_names:
			l.AddEntry(signal_histograms[signal_name], signal_name, "l")

		cname = "c_{}_{}_{}_{}".format(var, selection, jet_type, what)
		if logy:
			cname += "_logy"
		c = TCanvas(cname, var, 800, 1000)
		top = TPad("top", "top", 0., 0.5, 1., 1.)
		top.SetBottomMargin(0.02)
		top.Draw()
		top.cd()
		if logy:
			top.SetLogy()
		#bkgd_stack = data_histogram.Clone()
		#bkgd_stack.Reset()
		bkgd_stack.Draw("hist")
		bkgd_stack.GetXaxis().SetLabelSize(0)
		bkgd_stack.GetXaxis().SetTitleSize(0)
		bkgd_stack.GetYaxis().SetTitleSize(0.06)
		bkgd_stack.GetYaxis().SetTitleOffset(0.9)
		bkgd_stack.GetYaxis().SetLabelSize(0.06)
		bkgd_stack.GetYaxis().SetTitle("Events")
		ymax = max(data_histogram.GetMaximum(), total_bkgd_histogram.GetMaximum())
		if logy:
			ymin = 0.5
			ymax = ymax * 10
		else:
			ymin = 0.
			ymax = ymax * 1.3
		bkgd_stack.SetMinimum(ymin)
		bkgd_stack.SetMaximum(ymax)
		if x_range:
			bkgd_stack.GetXaxis().SetRangeUser(x_range[0], x_range[1])
		#frame_top.Draw("axis")
		#bkgd_stack.Draw("same")
		total_bkgd_histogram.SetMarkerStyle(20)
		total_bkgd_histogram.SetMarkerSize(0)
		total_bkgd_histogram.SetLineWidth(2)
		total_bkgd_histogram.SetLineColor(seaborn.GetColorRoot("dark", 1))
		total_bkgd_histogram.SetFillColor(0)
		total_bkgd_histogram.SetFillStyle(0)
		total_bkgd_histogram.Draw("hist same")
		data_histogram.SetMarkerSize(1)
		data_histogram.SetMarkerStyle(20)
		data_histogram.SetMarkerColor(1)
		data_histogram.SetLineWidth(1)
		data_histogram.SetLineColor(1)
		data_histogram.Draw("p same")
		for i, signal_name in enumerate(signal_names):
			signal_histograms[signal_name].SetLineWidth(2)
			signal_histograms[signal_name].SetLineStyle(2+i)
			signal_histograms[signal_name].SetLineColor(seaborn.GetColorRoot("dark", i))
			signal_histograms[signal_name].Draw("hist same")
		#frame_top.Draw("axis same")
		l.Draw()

		c.cd()
		bottom = TPad("bottom", "bottom", 0., 0., 1., 0.5)
		bottom.SetTopMargin(0.02)
		bottom.SetBottomMargin(0.2)
		bottom.Draw()
		bottom.cd()
		ratio_histogram = data_histogram.Clone()
		ratio_histogram.SetDirectory(0)
		ratio_histogram.Divide(total_bkgd_histogram)
		ratio_histogram.SetMinimum(0.)
		ratio_histogram.SetMaximum(3.)
		ratio_histogram.GetXaxis().SetTitle(style.axis_titles[var])
		ratio_histogram.GetXaxis().SetTitleSize(0.06)
		ratio_histogram.GetXaxis().SetLabelSize(0.06)
		ratio_histogram.GetYaxis().SetTitleSize(0.06)
		ratio_histogram.GetYaxis().SetTitleOffset(0.9)
		ratio_histogram.GetYaxis().SetLabelSize(0.06)
		ratio_histogram.GetYaxis().SetTitle("Data / Bkgd")
		if x_range:
			ratio_histogram.GetXaxis().SetRangeUser(x_range[0], x_range[1])
		ratio_histogram.Draw("p")

		c.cd()
		c.SaveAs("/uscms/home/dryu/DAZSLE/data/EventSelection/figures/{}.pdf".format(c.GetName()))
		c.SaveAs("/uscms/home/dryu/DAZSLE/data/EventSelection/figures/{}.eps".format(c.GetName()))
		c.SaveAs("/uscms/home/dryu/DAZSLE/data/EventSelection/figures/{}.C".format(c.GetName()))
		ROOT.SetOwnership(top, False)
		ROOT.SetOwnership(bottom, False)
		ROOT.SetOwnership(c, False)
		histogram_file.Close()

if __name__ == "__main__":
	vars = ["pfmet","dcsv","n2ddt","pt","eta","rho", "msd"]
	rebin = {"pfmet":1,"dcsv":4, "n2ddt":1, "pt":10, "eta":1, "rho":4, "msd":1}
	legend_positions = {"pfmet":"right","dcsv":"right","n2ddt":"right","pt":"right","eta":"right","rho":"left", "msd":"right"}
	x_ranges = {
		"pfmet":[0,500],
		"dcsv":[-1,1],
		"n2ddt":[-0.4, 0.2],
		"pt":[0,2000],
		"eta":[-3.,3.],
		"rho":[-7.5, -1.],
		"msd":[0., 400.]
	}
	selections = ["SR", "Preselection", "muCR"]
	backgrounds = {
		"SR":["qcd","tqq","wqq","zqq","hbb","stqq","vvqq"],
		"Preselection":["qcd","tqq","wqq","zqq","hbb","stqq","vvqq"],
		"muCR":["qcd","zll","wlnu","tqq","wqq","zqq","hbb","stqq","vvqq"]
	}
	jet_types = ["AK8", "CA15"]
	data_names = {"SR":"data_obs", "Preselection":"data_obs", "muCR":"data_singlemu"}
	for var in vars:
		for selection in selections:
			for jet_type in jet_types:
				DataMCPlot(var, selection, jet_type, data_name=data_names[selection], backgrounds=backgrounds[selection], rebin=rebin[var], legend_position=legend_positions[var], x_range=x_ranges[var])
				DataMCPlot(var, selection, jet_type, data_name=data_names[selection], backgrounds=backgrounds[selection], logy=True, rebin=rebin[var], legend_position=legend_positions[var], x_range=x_ranges[var])
