# Get signal acceptance and efficiencies
import os
import sys
from ROOT import *

signal_efficiencies = {
	"AK8":{
		"DMSbb":{
			50:0.136806951029,
			75:0.157919073083,
			100:0.160434230628,
			125:0.159514011064,
			150:0.156461418772,
			200:0.123577984376,
			250:0.0805671672485,
			300:0.0620419643308,
			400:0.0521823010331,
			500:0.0554893127909,
		},
	},
}

signal_efficiencies_tau21opt = {
	0.4:{
		"AK8":{
			"DMSbb":{
				50:0.0304686977255,
				75:0.0373338295892,
				100:0.0378419012467,
				125:0.037244396394,
				150:0.0355440923495,
				200:0.0242091066711,
				250:0.012191403632,
				300:0.00743227101759,
				400:0.00512983223818,
				500:0.00572437967501,
			},
		},
	},
	0.45:{
		"AK8":{
			"DMSbb":{
				50:0.0588442088153,
				75:0.0716359669079,
				100:0.0745850940775,
				125:0.0774270405423,
				150:0.0766496460957,
				200:0.058571837605,
				250:0.0305110935118,
				300:0.0199609211673,
				400:0.0145710108222,
				500:0.0147427499008,
			},
		},
	},
	0.5:{
		"AK8":{
			"DMSbb":{
				50:0.0949264914002,
				75:0.111356375121,
				100:0.114747472859,
				125:0.120210991655,
				150:0.11854080107,
				200:0.0914675530226,
				250:0.0524035406933,
				300:0.0370730924318,
				400:0.0285132289492,
				500:0.0302599428375,
			},
		},
	},
	0.525:{
		"AK8":{
			"DMSbb":{
				50:0.112896722747,
				75:0.131250569265,
				100:0.135933241689,
				125:0.14040159224,
				150:0.138755913056,
				200:0.107411081547,
				250:0.0639707571857,
				300:0.0471131698665,
				400:0.0375290930761,
				500:0.040850499897,
			},
		},
	},
	0.55:{
		"AK8":{
			"DMSbb":{
				50:0.132505441391,
				75:0.151837147169,
				100:0.155667001052,
				125:0.159751682832,
				150:0.157004302183,
				200:0.123025015815,
				250:0.0759606954668,
				300:0.0576685487438,
				400:0.047708954517,
				500:0.0510946165107,
			},
		},
	},
	0.575:{
		"AK8":{
			"DMSbb":{
				50:0.150526319266,
				75:0.171232217279,
				100:0.17584260076,
				125:0.177797146609,
				150:0.175450838234,
				200:0.138063481038,
				250:0.0880576791782,
				300:0.0684541903443,
				400:0.0581280379556,
				500:0.0623066512561,
			},
		},
	},
	0.6:{
		"AK8":{
			"DMSbb":{
				50:0.168630228859,
				75:0.191253571827,
				100:0.194250165792,
				125:0.195996267342,
				150:0.192992336744,
				200:0.151660399253,
				250:0.100342371748,
				300:0.0800118537691,
				400:0.0691918446641,
				500:0.0736779711085,
			},
		},
	},
	0.65:{
		"AK8":{
			"DMSbb":{
				50:0.202547945328,
				75:0.228900657797,
				100:0.228767521266,
				125:0.22926937767,
				150:0.223719890917,
				200:0.180957498266,
				250:0.125465727578,
				300:0.103836085208,
				400:0.0918927791718,
				500:0.09820209259,
			},
		},
	},
	0.7:{
		"AK8":{
			"DMSbb":{
				50:0.23370726668,
				75:0.260672572441,
				100:0.258661648355,
				125:0.257630155566,
				150:0.25165936477,
				200:0.206664552978,
				250:0.14977309266,
				300:0.127244577953,
				400:0.115288290603,
				500:0.120706008383,
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
				final = cutflow_histogram.GetBinContent(cutflow_histogram.GetNbinsX() - 1)
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
					final = cutflow_histogram.GetBinContent(cutflow_histogram.GetNbinsX() - 1)
					print "\t\t\t\t{}:{},".format(mass,float(final)/float(inclusive))
				print "\t\t\t},"
			print "\t\t},"
		print "\t},"
	print "}"
