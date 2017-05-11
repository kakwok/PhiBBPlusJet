#ifndef BaconData_h
#define BaconData_h

#include <typeinfo>
#include "DAZSLE/PhiBBPlusJet/interface/BaconTree.h"
#include "TMath.h"
#include "TH1D.h"
#include "TF1.h"
 /**
  * @brief      Class for exposing data from bacon ntuples.
  */
 

class BaconData : public BaconTree {
public:

	BaconData(TTree *tree=0);

	~BaconData();

	Int_t GetEntry(Long64_t entry);

	Double_t PUPPIweight(double pt, double eta) const;

public:
	// Computed variables
	Double_t AK8Puppijet0_tau21DDT;
	Double_t CA15Puppijet0_tau21DDT;
	Double_t AK8Puppijet0_rho;
	Double_t CA15Puppijet0_rho;
	Double_t AK8Puppijet0_N2DDT;
	Double_t CA15Puppijet0_N2DDT;
	Double_t CA15CHSjet0_N2DDT;
	Double_t AK8Puppijet0_msd_puppi;
	Double_t CA15Puppijet0_msd_puppi;
	Double_t puppet_JESUp;
	Double_t puppet_JESDown;
	Double_t puppet_JERUp;
	Double_t puppet_JERDown;
	Double_t pfmet_JESUp;
	Double_t pfmet_JESDown;
	Double_t pfmet_JERUp;
	Double_t pfmet_JERDown;
private:
	TH1D* n2_ddt_transformation_;
	TF1* puppi_corr_gen_;
	TF1* puppi_corr_reco_cen_;
	TF1* puppi_corr_reco_for_;

};


#endif