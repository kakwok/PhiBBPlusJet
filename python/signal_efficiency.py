# Get signal acceptance and efficiencies
import os
import sys
from ROOT import *

signal_efficiencies = {
	"AK8":{
		"DMSbb":{
			50:0.0713642352613,
			75:0.0777450690553,
			100:0.0728258522185,
			125:0.0658257296402,
			150:0.0558254982014,
			200:0.0307416452023,
			250:0.0115742247371,
			300:0.00531829860311,
			400:0.00333839528453,
			500:0.00359478184814,
		},
	},
}
signal_efficiencies_tau21opt = {
	0.4:{
		"AK8":{
			"DMSbb":{
				50:0.0188165526394,
				75:0.0213947609298,
				100:0.0223646412369,
				125:0.0202394331215,
				150:0.0170136790465,
				200:0.0082808064753,
				250:0.00323309355103,
				300:0.00111415604497,
				400:0.000358411244289,
				500:0.000372646669893,
			},
		},
	},
	0.45:{
		"AK8":{
			"DMSbb":{
				50:0.0344871573573,
				75:0.0407089893034,
				100:0.0414181126831,
				125:0.0388851768781,
				150:0.0341278988161,
				200:0.0186344816075,
				250:0.00677267632485,
				300:0.00262510988437,
				400:0.00107385794377,
				500:0.00115519999469,
			},
		},
	},
	0.5:{
		"AK8":{
			"DMSbb":{
				50:0.0531323477988,
				75:0.0604056444118,
				100:0.059022932101,
				125:0.0558350712519,
				150:0.0476733647053,
				200:0.0265883606382,
				250:0.0095512397893,
				300:0.0038635395096,
				400:0.00193621237231,
				500:0.00246184777391,
			},
		},
	},
	0.525:{
		"AK8":{
			"DMSbb":{
				50:0.0619059186565,
				75:0.0691305955629,
				100:0.0666431839177,
				125:0.0620201429633,
				150:0.0530657323129,
				200:0.0290232299094,
				250:0.0105032338176,
				300:0.00448944124422,
				400:0.0025057033187,
				500:0.00282052947208,
			},
		},
	},
	0.55:{
		"AK8":{
			"DMSbb":{
				50:0.0704827494668,
				75:0.07668405047,
				100:0.0729961775006,
				125:0.0675638628713,
				150:0.057076922442,
				200:0.0311376205278,
				250:0.0112992358303,
				300:0.00504226130954,
				400:0.00312594592639,
				500:0.00330149544931,
			},
		},
	},
	0.575:{
		"AK8":{
			"DMSbb":{
				50:0.0780836379395,
				75:0.0838586837215,
				100:0.0790884051769,
				125:0.0719807276067,
				150:0.060579602056,
				200:0.0331018962091,
				250:0.0120592359013,
				300:0.00561874376786,
				400:0.00368668736202,
				500:0.00386303667601,
			},
		},
	},
	0.6:{
		"AK8":{
			"DMSbb":{
				50:0.0855064120463,
				75:0.0910060975132,
				100:0.0836648164578,
				125:0.0764335211807,
				150:0.0636304566807,
				200:0.0344455243341,
				250:0.0127577711995,
				300:0.0061394842563,
				400:0.0041781480136,
				500:0.004378220162,
			},
		},
	},
	0.65:{
		"AK8":{
			"DMSbb":{
				50:0.0977622403189,
				75:0.101710893414,
				100:0.0919183490754,
				125:0.0814178714082,
				150:0.0680077143226,
				200:0.0364755488221,
				250:0.0139267798089,
				300:0.00705356220278,
				400:0.00496730174115,
				500:0.00545292651204,
			},
		},
	},
	0.7:{
		"AK8":{
			"DMSbb":{
				50:0.106891553117,
				75:0.109092866288,
				100:0.0972033940684,
				125:0.08537479423,
				150:0.0708783790406,
				200:0.0381559653971,
				250:0.014661718542,
				300:0.00775487498782,
				400:0.0059075609764,
				500:0.00620085213362,
			},
		},
	},
}

if __name__ == "__main__":
	# Get the signal efficiencies from cutflow histograms and print
	jet_types = ["AK8"]
	models = ["DMSbb"]
	masses = [50, 75, 100, 125, 150, 200, 250, 300, 400, 500]
	print "signal_efficiencies = {"
	for jet_type in jet_types:
		print "\t\"{}\":{{".format(jet_type)
		for model in models:
			print "\t\t\"{}\":{{".format(model)
			for mass in masses:
				histogram_file = TFile("~/DAZSLE/data/LimitSetting/InputHistograms_{}{}_AK8.root".format(model, mass), "READ")
				cutflow_histogram = histogram_file.Get("CutFlowCounter_EventSelector_SR_weighted")
				inclusive = cutflow_histogram.GetBinContent(1)
				pass_histogram = histogram_file.Get("h_SR_{}_pass".format(jet_type))
				final = pass_histogram.Integral()
				print "\t\t\t{}:{},".format(mass,float(final)/float(inclusive))
			print "\t\t},"
		print "\t},"
	print "}"

	# tau21 optimization
	tau21_values = [0.4, 0.45, 0.5, 0.525, 0.55, 0.575, 0.6, 0.65, 0.7]

	print "signal_efficiencies_tau21opt = {"
	for tau21_value in tau21_values:
		print "\t{}:{{".format(tau21_value)
		for jet_type in jet_types:
			print "\t\t\"{}\":{{".format(jet_type)
			for model in models:
				print "\t\t\t\"{}\":{{".format(model)
				for mass in masses:
					histogram_file = TFile("~/DAZSLE/data/LimitSetting/InputHistograms_{}{}_AK8.root".format(model, mass), "READ")
					cutflow_histogram = histogram_file.Get("CutFlowCounter_EventSelector_SR_tau21ddt{}_weighted".format(tau21_value))
					inclusive = cutflow_histogram.GetBinContent(1)
					pass_histogram = histogram_file.Get("h_SR_tau21ddt_{}_{}_pass".format(tau21_value, jet_type))
					final = pass_histogram.Integral()
					print "\t\t\t\t{}:{},".format(mass,float(final)/float(inclusive))
				print "\t\t\t},"
			print "\t\t},"
		print "\t},"
	print "}"
