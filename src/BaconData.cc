#ifndef BaconData_cc
#define BaconData_cc

#include "DAZSLE/PhiBBPlusJet/interface/BaconData.h"

BaconData::BaconData(TTree *tree) : BaconTree(tree) {
	// Histogram for N2 DDT
	TFile *f_n2ddt = new TFile("$CMSSW_BASE/src/DAZSLE/ZPrimePlusJet/analysis/ZqqJet/h3_n2ddt_26eff_36binrho11pt_Spring16.root","read");
	n2_ddt_transformation_ = (TH1D*)f_n2ddt->Get("h2ddt");
	n2_ddt_transformation_->SetDirectory(0);
	f_n2ddt->Close();
	delete f_n2ddt;

}

BaconData::~BaconData() {
}

Int_t BaconData::GetEntry(Long64_t entry) {
	// Clear previous event

	// Load new event
	Int_t ret = fChain->GetEntry(entry);
	return ret;
}


#endif