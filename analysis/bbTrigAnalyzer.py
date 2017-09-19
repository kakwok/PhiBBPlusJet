import os
import sys
import ROOT
from DAZSLE.PhiBBPlusJet.analysis_base import AnalysisBase
import DAZSLE.PhiBBPlusJet.analysis_configuration as config
from DAZSLE.PhiBBPlusJet.bacon_event_selector import *
from math import ceil, sqrt,floor
import array
import time
import numpy

import ROOT
from ROOT import *
gInterpreter.Declare("#include \"MyTools/RootUtils/interface/SeabornInterface.h\"")
gInterpreter.Declare("#include \"MyTools/RootUtils/interface/HistogramManager.h\"")
gSystem.Load(os.path.expandvars("$CMSSW_BASE/lib/$SCRAM_ARCH/libMyToolsRootUtils.so"))
gInterpreter.Declare("#include \"MyTools/AnalysisTools/interface/EventSelector.h\"")
gSystem.Load(os.path.expandvars("$CMSSW_BASE/lib/$SCRAM_ARCH/libMyToolsAnalysisTools.so"))
ROOT.gInterpreter.Declare("#include \"DAZSLE/PhiBBPlusJet/interface/BaconData.h\"")
ROOT.gInterpreter.Declare("#include \"DAZSLE/PhiBBPlusJet/interface/BaconEventCutFunctions.h\"")
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
        self._data = BaconData(self._chain)
        self._output_path = ""
        self._input_nevents = 0
        self._jet_type = "AK8"
        self._doBlinding    = True
        self._hasTriggers   = True

    # Overload add_file to extract the number of input events to the skims, stored in histogram NEvents in the same file as the trees
    def add_file(self, filename):
        super(TestPyEventSelector, self).add_file(filename)
        f = ROOT.TFile.Open(filename, "READ")
        self._input_nevents += f.Get("NEvents").Integral()
        f.Close()

    def set_output_path(self, output_path):
        self._output_path = output_path
        os.system("mkdir -pv {}".format(os.path.dirname(self._output_path)))

    def set_doBlinding(self, doBlinding):
        print "Setting doBlinging to "+ str(doBlinding)
        self._doBlinding = doBlinding
    def set_hasTriggers(self, hasTriggers):
        print "Setting hasTriggers to "+ str(hasTriggers)
        self._hasTriggers = hasTriggers 

    def start(self):
        self._processed_events = 0

        # Histograms
        self._pt_bins = array.array("d", [350.,400.,450., 500.,550.,600.,675.,800.,1000.])

        self._histograms = ROOT.Root.HistogramManager()
        self._histograms.AddPrefix("h_")

        self._histograms.AddTH1F("input_nevents", "input_nevents", "", 1, -0.5, 0.5)
        self._histograms.GetTH1F("input_nevents").SetBinContent(1, self._input_nevents)
        self._histograms.AddTH1D("processed_nevents", "processed_nevents", "", 1, -0.5, 0.5)

        self._histograms.AddTH1D("pass_mSD", "pass_mSD", "", 23, 40, 201)
        self._histograms.AddTH1D("fail_mSD", "fail_mSD", "", 23, 40, 201)
        self._histograms.AddTH1D("AK8Puppijet0_pt", "AK8Puppijet0_pt", "p_{T} [GeV]", 200, 0., 2000.)
        self._histograms.AddTH2D("pt_mSD", "AK8Puppijet0_pt_vs_mSD;m_{{SD}}^{{PUPPI}} [GeV] ;p_{{T}} [GeV]","m_{SD}^{PUPPI} [GeV]",23,40,201,"p_{T} [GeV]", len(self._pt_bins)-1, self._pt_bins)

        self._histograms.AddTH1D("bbTrig_pass_mSD"       , "pass_mSD", "", 23, 40, 201)
        self._histograms.AddTH1D("bbTrig_fail_mSD"       , "fail_mSD", "", 23, 40, 201)
        self._histograms.AddTH1D("bbTrig_AK8Puppijet0_pt", "AK8Puppijet0_pt", "p_{T} [GeV]", 200, 0., 2000.)
        self._histograms.AddTH2D("bbTrig_pt_mSD", "AK8Puppijet0_pt_vs_mSD;m_{{SD}}^{{PUPPI}} [GeV] ;p_{{T}} [GeV]","m_{SD}^{PUPPI} [GeV]",23,40,201,"p_{T} [GeV]", len(self._pt_bins)-1, self._pt_bins)
        
        self._histograms.AddTH2D("Trig_pt_mSD_base"       , "AK8Puppijet0_pt_vs_mSD;m_{{SD}}^{{PUPPI}} [GeV] ;p_{{T}} [GeV]","m_{SD}^{PUPPI} [GeV]",15,0,300,"p_{T} [GeV]",20 ,0.,1000.0)
        self._histograms.AddTH2D("Trig_pt_mSD_TrimMass_bb", "AK8Puppijet0_pt_vs_mSD;m_{{SD}}^{{PUPPI}} [GeV] ;p_{{T}} [GeV]","m_{SD}^{PUPPI} [GeV]",15,0,300,"p_{T} [GeV]",20 ,0.,1000.0)
        self._histograms.AddTH2D("Trig_pt_mSD_TrimMass"   , "AK8Puppijet0_pt_vs_mSD;m_{{SD}}^{{PUPPI}} [GeV] ;p_{{T}} [GeV]","m_{SD}^{PUPPI} [GeV]",15,0,300,"p_{T} [GeV]",20 ,0.,1000.0)
        self._histograms.AddTH2D("Trig_pt_mSD_bb"         , "AK8Puppijet0_pt_vs_mSD;m_{{SD}}^{{PUPPI}} [GeV] ;p_{{T}} [GeV]","m_{SD}^{PUPPI} [GeV]",15,0,300,"p_{T} [GeV]",20 ,0.,1000.0)
        self._histograms.AddTH1D("triggerbits", "triggerbits", "", 20, 0, 20)


        # Event selections
        self._event_selector = BaconEventSelector("standardHbb")
        self._event_selector.add_cut("Min_AK8Puppijet0_msd", 40.)
        self._event_selector.add_cut("Min_AK8Puppijet0_pt", {"Min_AK8Puppijet0_pt":450., "systematic":"nominal"})
        self._event_selector.add_cut("AK8Puppijet0_isTightVJet", None)
        self._event_selector.add_cut("Max_neleLoose", 0)
        self._event_selector.add_cut("Max_nmuLoose", 0)
        self._event_selector.add_cut("Max_ntau", 0)
        self._event_selector.add_cut("Max_puppet", {"Max_puppet":180., "systematic":"nominal"})
        self._event_selector.add_cut("Max_AK8Puppijet0_N2DDT", 0)
        self._event_selector.add_cut("AK8Puppijet0_rho", None)

        self._doubleB_event_selector = BaconEventSelector("doubleBtrigger")
        self._doubleB_event_selector.add_cut("Min_AK8Puppijet0_msd", 40.)
        self._doubleB_event_selector.add_cut("Min_AK8Puppijet0_pt", {"Min_AK8Puppijet0_pt":350., "systematic":"nominal"}) # lower the pT threshold
        self._doubleB_event_selector.add_cut("AK8Puppijet0_isTightVJet", None)
        self._doubleB_event_selector.add_cut("Max_neleLoose", 0)
        self._doubleB_event_selector.add_cut("Max_nmuLoose", 0)
        self._doubleB_event_selector.add_cut("Max_ntau", 0)
        self._doubleB_event_selector.add_cut("Max_puppet", {"Max_puppet":180., "systematic":"nominal"})
        self._doubleB_event_selector.add_cut("Max_AK8Puppijet0_N2DDT", 0)
        self._doubleB_event_selector.add_cut("AK8Puppijet0_rho", None)

        self._offline_event_selector = BaconEventSelector("offlineCuts")
        self._offline_event_selector.add_cut("Min_AK8Puppijet0_pt", {"Min_AK8Puppijet0_pt":150., "systematic":"nominal"}) # lower the pT threshold
        self._offline_event_selector.add_cut("AK8Puppijet0_isTightVJet", None)
        self._offline_event_selector.add_cut("Max_neleLoose", 0)
        self._offline_event_selector.add_cut("Max_nmuLoose", 0)
        self._offline_event_selector.add_cut("Max_ntau", 0)
        self._doubleB_event_selector.add_cut("Max_pfmet", {"Max_pfmet":140., "systematic":"nominal"})
        self._offline_event_selector.add_cut("Max_AK8Puppijet0_N2DDT", 0)
        self._offline_event_selector.add_cut("AK8Puppijet0_rho", None)


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
            self._doubleB_event_selector.process_event(self._data, 1.)
            self._offline_event_selector.process_event(self._data, 1.)

            self._histograms.GetTH1D("triggerbits").Fill(self._data.triggerBits)
            triggerbit  = self._data.triggerBits
            fatjet_pt   = self._data.AK8Puppijet0_pt
            fatjet_msd  = self._data.AK8Puppijet0_msd_puppi
            fatjet_dcsv = self._data.AK8CHSjet0_doublecsv

            if (self._event_selector.event_pass() and ((triggerbit & 2)or(not self._hasTriggers))):
                if fatjet_dcsv > 0.9:
                    if not( (self._doBlinding) and (fatjet_msd > 117.0 and fatjet_msd < 131.0)):
                        self._histograms.GetTH1D("pass_mSD").Fill(fatjet_msd)
                        self._histograms.GetTH1D("AK8Puppijet0_pt").Fill(fatjet_pt)
                        self._histograms.GetTH2D("pt_mSD").Fill(fatjet_msd,fatjet_pt)
                else:
                    self._histograms.GetTH1D("fail_mSD").Fill(fatjet_msd)
            if (self._doubleB_event_selector.event_pass() and (((triggerbit & 2) or (triggerbit & 16))or(not self._hasTriggers)) ):
                if fatjet_dcsv > 0.9:
                    if not( (self._doBlinding) and (fatjet_msd > 117.0 and fatjet_msd < 131.0)):
                        self._histograms.GetTH1D("bbTrig_pass_mSD").Fill(fatjet_msd)
                        self._histograms.GetTH1D("bbTrig_AK8Puppijet0_pt").Fill(fatjet_pt)
                        self._histograms.GetTH2D("bbTrig_pt_mSD").Fill(fatjet_msd,fatjet_pt)
                else:
                    self._histograms.GetTH1D("bbTrig_fail_mSD").Fill(fatjet_msd)
            if self._offline_event_selector.event_pass():
                self._histograms.GetTH2D("Trig_pt_mSD_base").Fill(fatjet_msd,fatjet_pt)
                if (triggerbit & 2):
                    self._histograms.GetTH2D("Trig_pt_mSD_TrimMass").Fill(fatjet_msd,fatjet_pt)
                if (triggerbit & 16):
                    self._histograms.GetTH2D("Trig_pt_mSD_bb").Fill(fatjet_msd,fatjet_pt)
                if (triggerbit & 16) or (triggerbit & 2):
                    self._histograms.GetTH2D("Trig_pt_mSD_TrimMass_bb").Fill(fatjet_msd,fatjet_pt)
                    
    def finish(self):
        if self._output_path == "":
            self._output_path = os.path.expandvars("$CMSSW_BASE/src/DAZSLE/PhiBBPlusJet/output/TestPyEventSelector.root".format(time.time))
            print "[SignalCutflow::finish] WARNING : Output path was not provided! Saving to {}".format(self._output_path)
        print "[SignalCutflow::finish] INFO : Saving histograms to {}".format(self._output_path)
        f_out = ROOT.TFile(self._output_path, "RECREATE")
        self._histograms.SaveAll(f_out)
        self._event_selector.print_cutflow()
        self._event_selector.make_cutflow_histograms(f_out)
        self._event_selector.save_nminusone_histograms(f_out)
        self._doubleB_event_selector.print_cutflow()
        self._doubleB_event_selector.make_cutflow_histograms(f_out)
        self._doubleB_event_selector.save_nminusone_histograms(f_out)

        f_out.Close()

def readFile(fname):
    lines=[]
    for x in open(fname):
        if not x[0]=="#": lines.append(x.strip())
    return lines
        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Produce')
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('--samples', type=str, help="Sample name(s), comma separated. Must be a key in analysis_configuration.skims.")
    input_group.add_argument('--files'  , type=str, help="Input file name(s), comma separated")

    parser.add_argument('--outputTag'  , type=str, help="File extenstion output files")
    parser.add_argument('--output_folder'  , type=str, help="Output location")
    parser.add_argument('--n_jobs'      , type=int, default=4, help="For --run, specify the number of parallel jobs.")
    parser.add_argument('--run'         , action='store_true', help="For --run, specify the number of parallel jobs.")
    parser.add_argument('--bsub'        , action='store_true', help="Make script and Submit with bsub .")
    parser.add_argument('--dryRun'      , action='store_true', help="Do not submit the jobs")
    parser.add_argument('--label'       , type=str, help="If running with --files, need to specify a label manually, in lieu of the sample names, for the output file naming.")
    args = parser.parse_args()

    inputFolder = "inputFiles/"    
    samples = ["JetHT","ggH","QCD"]
    sample_files = {}
    #sample_files["JetHT"] = ["/afs/cern.ch/user/k/kakwok/eos/Hbb/Baconbits/zprimebits-v12.06/JetHTRun2016G_03Feb2017_v1_v4/Output.root_job0_file0.root"]
    #sample_files["JetHT"] = [x.strip() for x in open(os.path.expandvars("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/data/skim_directory/lxplus/JetHTRun2016G.txt"))]
    sample_files["JetHT"]  = readFile(inputFolder+"2016B_ver1.txt")
    sample_files["JetHT"] += readFile(inputFolder+"2016B_ver2.txt")
    sample_files["JetHT"] += readFile(inputFolder+"2016C.txt")
    sample_files["JetHT"] += readFile(inputFolder+"2016D.txt")
    sample_files["JetHT"] += readFile(inputFolder+"2016E.txt")
    sample_files["JetHT"] += readFile(inputFolder+"2016F.txt")
    sample_files["JetHT"] += readFile(inputFolder+"2016G.txt")
    sample_files["JetHT"] += readFile(inputFolder+"2016H_ver2.txt")
    sample_files["JetHT"] += readFile(inputFolder+"2016H_ver3.txt")
    
    sample_files["ggH"]  = readFile(inputFolder+"GluGluHToBB_M125_13TeV_powheg_pythia8_v4.txt")
    sample_files["ggH"] += readFile(inputFolder+"GluGluHToBB_M125_13TeV_powheg_pythia8_ext_v4.txt")
    
    sample_files["QCD"]  =  readFile(inputFolder+"QCD_HT1000to1500_13TeV_ext.txt")
    sample_files["QCD"]  += readFile(inputFolder+"QCD_HT1000to1500_13TeV.txt"    )
    sample_files["QCD"]  += readFile(inputFolder+"QCD_HT700to1000_13TeV_ext.txt" )
    sample_files["QCD"]  += readFile(inputFolder+"QCD_HT700to1000_13TeV.txt"     )
    sample_files["QCD"]  += readFile(inputFolder+"QCD_HT50to100_13TeV.txt"       )
    sample_files["QCD"]  += readFile(inputFolder+"QCD_HT500to700_13TeV_ext.txt"  )
    sample_files["QCD"]  += readFile(inputFolder+"QCD_HT500to700_13TeV.txt"      )
    sample_files["QCD"]  += readFile(inputFolder+"QCD_HT300to500_13TeV_ext.txt"  )
    sample_files["QCD"]  += readFile(inputFolder+"QCD_HT300to500_13TeV.txt"      )
    sample_files["QCD"]  += readFile(inputFolder+"QCD_HT200to300_13TeV_ext.txt"  )
    sample_files["QCD"]  += readFile(inputFolder+"QCD_HT200to300_13TeV.txt"      )
    sample_files["QCD"]  += readFile(inputFolder+"QCD_HT2000toInf_13TeV_ext.txt" )
    sample_files["QCD"]  += readFile(inputFolder+"QCD_HT2000toInf_13TeV.txt"     )
    sample_files["QCD"]  += readFile(inputFolder+"QCD_HT1500to2000_13TeV_ext.txt")
    sample_files["QCD"]  += readFile(inputFolder+"QCD_HT1500to2000_13TeV.txt"    )
    sample_files["QCD"]  += readFile(inputFolder+"QCD_HT100to200_13TeV.txt"      )  

    if args.run or args.bsub:
        # Make a list of input samples and files
        samples = []
        if args.samples:
            samples = args.samples.split(",")
        elif args.files:    
            files = args.files.split(",")
            for filename in files:
                if args.label:
                    this_sample = args.label
                    sample_files[this_sample] = []
                else:
                    print "[event_selection_histograms] ERROR : When running with --files option, you must specify a label for the output!"
                    sys.exit(1)
                sample_files[this_sample].append(filename)
            samples.append(args.label)
        print "List of samples= ", samples

    if args.run:
        for sample in samples:
            print "\n *** Running sample {}".format(sample)
            if "JetHT" in sample :
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
            print "Constucting the analyzer with tree name ={} ".format(tree_name)
            tester = TestPyEventSelector(sample, tree_name=tree_name)
            for filename in sample_files[sample]:
                print "Input file {}".format(filename)
                tester.add_file(filename)
            if args.output_folder and args.outputTag:
                tester.set_output_path("{}/TestPyEventSelector_{}_{}.root".format(args.output_folder, sample,args.outputTag))
            if not (sample in "JetHT"):
                tester.set_doBlinding(False)
            if ("QCD" in sample):
                tester.set_hasTriggers(False)
            tester.start()
            tester.run()
            tester.finish()
    if args.bsub:
        import time
        for sample in samples:
            start_directory = os.getcwd()
            job_tag = "job_{}_{}".format(sample, int(floor(time.time())))
            submission_directory = job_tag
            os.system("mkdir -pv {}".format(submission_directory))
            os.chdir(submission_directory)

            queue  = "1nd"
            files_per_job = 5
            n_jobs = int(math.ceil(1. * len(sample_files[sample]) / files_per_job))
            print "Working on sample ={}, total files = {} , splitting {} files per job, creating {} jobs.".format(sample, len(sample_files[sample]), files_per_job,n_jobs)
            split_list = numpy.array_split(sample_files[sample], n_jobs)
            for i,files in enumerate(split_list):
                filesCSV =','.join(map(str, files))
                job_command = "python test_pyeventselector.py --run --files={} --output_folder={} --outputTag={} --label={}".format(filesCSV,submission_directory,job_tag+"_"+str(i),sample)
                job_script_name  = job_tag+"_"+str(i)+".sh"
                job_script = open(job_script_name,"w")
                job_script.write("#!/bin/sh\n")
                job_script.write("cd /afs/cern.ch/user/k/kakwok/work/public/Hbb_ISR/CMSSW_7_4_15/src/DAZSLE/PhiBBPlusJet/analysis\n")
                job_script.write("echo $PWD\n")
                job_script.write("eval `scramv1 runtime -sh`\n")
                job_script.write("echo \"Running python test_pyeventselector.py\"\n")
                job_script.write(job_command+"\n")
                os.system("chmod 755 {}".format(job_script_name))
                submit_cmd="bsub -q {} -J {} {}".format(queue,job_tag+"_"+str(i),job_script_name)
                print submit_cmd
                if not args.dryRun:
                    os.system(submit_cmd)
