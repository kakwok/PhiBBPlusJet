#ifndef BaconData_h
#define BaconData_h

#include <typeinfo>
#include "DAZSLE/PhiBBPlusJet/interface/BaconTree.h"
#include "TMath.h"
#include "TH1D.h"
 /**
  * @brief      Class for exposing data from bacon ntuples.
  */
 

class BaconData : public BaconTree {
public:

	BaconData(TTree *tree=0);

	~BaconData();

	Int_t GetEntry(Long64_t entry);

	// Helper functions for exposing data without having to know branch names...
	inline Double_t AK8Puppijet0_tau21DDT() const {
		return AK8Puppijet0_tau21 + 0.063*TMath::Log(AK8Puppijet0_msd*AK8Puppijet0_msd/AK8Puppijet0_pt);
	}

	inline Double_t CA15Puppijet0_tau21DDT() const {
		return CA15Puppijet0_tau21 + 0.063*TMath::Log(CA15Puppijet0_msd*CA15Puppijet0_msd/CA15Puppijet0_pt);
	}

	inline Double_t AK8Puppijet0_rho() const {
		return 2 * TMath::Log(AK8Puppijet0_msd/ AK8Puppijet0_pt);
	}

	inline Double_t AK8Puppijet0_N2DDT() const {
		int rho_index = n2_ddt_transformation_->GetXaxis()->FindBin(AK8Puppijet0_rho());
		if (rho_index > n2_ddt_transformation_->GetXaxis()->GetNbins()) {
			rho_index = n2_ddt_transformation_->GetXaxis()->GetNbins();
		} else if (rho_index <= 0) {
			rho_index = 1;
		}

		int pt_index = n2_ddt_transformation_->GetYaxis()->FindBin(AK8Puppijet0_pt);
		if (pt_index > n2_ddt_transformation_->GetYaxis()->GetNbins()) {
			pt_index = n2_ddt_transformation_->GetYaxis()->GetNbins();
		} else if (pt_index <= 0) {
			pt_index = 1;
		}
		return AK8Puppijet0_N2sdb1 - n2_ddt_transformation_->GetBinContent(rho_index, pt_index);
	}
private:
	TH1D* n2_ddt_transformation_;

};


#endif