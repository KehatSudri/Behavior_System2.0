#pragma once
#ifndef __SessionController__
#define __SessionController__
#include "SessionControls.h"
#include "LogFileWriter.h"
#include <msclr/marshal_cppstd.h>

namespace BSRunner {
	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Windows::Forms;
	using namespace System::Runtime::InteropServices;
	using namespace System::Data;
	using namespace System::Drawing;

	public ref class SessionController : public System::Windows::Forms::Form {
	public:
		SessionController(int argc, char* argv[]) {
			_configFilePath = argv[1];
			LogFileWriter::getInstance().setSessionName(argv[2]);
			InitializeComponent();
		}

	protected:
		~SessionController() {
			if (components) {
				delete _configFilePath;
				delete components;
			}
		}

	private:
		char* _configFilePath;
		System::ComponentModel::Container^ components;
		System::Windows::Forms::Button^ StartBtn;
		System::Windows::Forms::Button^ PauseBtn;
		System::Windows::Forms::Button^ ResumeBtn;
		System::Windows::Forms::Button^ RewardBtn;
		System::Windows::Forms::Button^ FinishBtn;
		System::Windows::Forms::Button^ NextTrailBtn;


		System::Windows::Forms::Panel^ NextTrialBtn;

#pragma region Windows Form Designer generated code
		void InitializeComponent(void) {
			this->StartBtn = (gcnew System::Windows::Forms::Button());
			this->PauseBtn = (gcnew System::Windows::Forms::Button());
			this->ResumeBtn = (gcnew System::Windows::Forms::Button());
			this->RewardBtn = (gcnew System::Windows::Forms::Button());
			this->FinishBtn = (gcnew System::Windows::Forms::Button());
			this->NextTrialBtn = (gcnew System::Windows::Forms::Panel());
			this->NextTrailBtn = (gcnew System::Windows::Forms::Button());
			this->NextTrialBtn->SuspendLayout();
			this->SuspendLayout();
			// 
			// StartBtn
			// 
			this->StartBtn->Anchor = System::Windows::Forms::AnchorStyles::None;
			this->StartBtn->Location = System::Drawing::Point(19, 13);
			this->StartBtn->Name = L"StartBtn";
			this->StartBtn->Size = System::Drawing::Size(199, 35);
			this->StartBtn->TabIndex = 0;
			this->StartBtn->Text = L"Start";
			this->StartBtn->UseVisualStyleBackColor = true;
			this->StartBtn->Click += gcnew System::EventHandler(this, &SessionController::StartBtn_Click);
			// 
			// PauseBtn
			// 
			this->PauseBtn->Anchor = System::Windows::Forms::AnchorStyles::None;
			this->PauseBtn->Location = System::Drawing::Point(19, 65);
			this->PauseBtn->Name = L"PauseBtn";
			this->PauseBtn->Size = System::Drawing::Size(92, 35);
			this->PauseBtn->TabIndex = 1;
			this->PauseBtn->Text = L"Pause";
			this->PauseBtn->UseVisualStyleBackColor = true;
			this->PauseBtn->Click += gcnew System::EventHandler(this, &SessionController::PauseBtn_Click);
			// 
			// ResumeBtn
			// 
			this->ResumeBtn->Anchor = System::Windows::Forms::AnchorStyles::None;
			this->ResumeBtn->Location = System::Drawing::Point(126, 65);
			this->ResumeBtn->Name = L"ResumeBtn";
			this->ResumeBtn->Size = System::Drawing::Size(92, 35);
			this->ResumeBtn->TabIndex = 2;
			this->ResumeBtn->Text = L"Resume";
			this->ResumeBtn->UseVisualStyleBackColor = true;
			this->ResumeBtn->Click += gcnew System::EventHandler(this, &SessionController::ResumeBtn_Click);
			// 
			// RewardBtn
			// 
			this->RewardBtn->Anchor = System::Windows::Forms::AnchorStyles::None;
			this->RewardBtn->Location = System::Drawing::Point(19, 119);
			this->RewardBtn->Name = L"RewardBtn";
			this->RewardBtn->Size = System::Drawing::Size(199, 35);
			this->RewardBtn->TabIndex = 3;
			this->RewardBtn->Text = L"Give Reward";
			this->RewardBtn->UseVisualStyleBackColor = true;
			this->RewardBtn->Click += gcnew System::EventHandler(this, &SessionController::RewardBtn_Click);
			// 
			// FinishBtn
			// 
			this->FinishBtn->Anchor = System::Windows::Forms::AnchorStyles::None;
			this->FinishBtn->Location = System::Drawing::Point(19, 230);
			this->FinishBtn->Name = L"FinishBtn";
			this->FinishBtn->Size = System::Drawing::Size(199, 35);
			this->FinishBtn->TabIndex = 4;
			this->FinishBtn->Text = L"Finish";
			this->FinishBtn->UseVisualStyleBackColor = true;
			this->FinishBtn->Click += gcnew System::EventHandler(this, &SessionController::FinishBtn_Click);
			// 
			// NextTrialBtn
			// 
			this->NextTrialBtn->Anchor = static_cast<System::Windows::Forms::AnchorStyles>((((System::Windows::Forms::AnchorStyles::Top | System::Windows::Forms::AnchorStyles::Bottom)
				| System::Windows::Forms::AnchorStyles::Left)
				| System::Windows::Forms::AnchorStyles::Right));
			this->NextTrialBtn->Controls->Add(this->NextTrailBtn);
			this->NextTrialBtn->Controls->Add(this->RewardBtn);
			this->NextTrialBtn->Controls->Add(this->StartBtn);
			this->NextTrialBtn->Controls->Add(this->ResumeBtn);
			this->NextTrialBtn->Controls->Add(this->FinishBtn);
			this->NextTrialBtn->Controls->Add(this->PauseBtn);
			this->NextTrialBtn->Location = System::Drawing::Point(12, 12);
			this->NextTrialBtn->Name = L"NextTrialBtn";
			this->NextTrialBtn->Size = System::Drawing::Size(235, 283);
			this->NextTrialBtn->TabIndex = 5;
			// 
			// NextTrailBtn
			// 
			this->NextTrailBtn->Anchor = System::Windows::Forms::AnchorStyles::None;
			this->NextTrailBtn->Location = System::Drawing::Point(19, 178);
			this->NextTrailBtn->Name = L"NextTrailBtn";
			this->NextTrailBtn->Size = System::Drawing::Size(199, 35);
			this->NextTrailBtn->TabIndex = 5;
			this->NextTrailBtn->Text = L"Next Trial";
			this->NextTrailBtn->UseVisualStyleBackColor = true;
			this->NextTrailBtn->Click += gcnew System::EventHandler(this, &SessionController::NextTrialBtn_click);
			// 
			// SessionController
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(6, 13);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(257, 307);
			this->Controls->Add(this->NextTrialBtn);
			this->Name = L"SessionController";
			this->Text = L"Control Board";
			this->Load += gcnew System::EventHandler(this, &SessionController::SessionControlPanel_Load);
			this->NextTrialBtn->ResumeLayout(false);
			this->ResumeLayout(false);

		}
#pragma endregion
	private: System::Void PauseBtn_Click(System::Object^ sender, System::EventArgs^ e) {
		SessionControls::getInstance().pauseSession();
	}
	private: System::Void StartBtn_Click(System::Object^ sender, System::EventArgs^ e) {
		SessionControls::getInstance().startSession(_configFilePath);
	}
	private: System::Void ResumeBtn_Click(System::Object^ sender, System::EventArgs^ e) {
		SessionControls::getInstance().resumeSession();
	}
	private: System::Void RewardBtn_Click(System::Object^ sender, System::EventArgs^ e) {
		SessionControls::getInstance().giveReward();
	}
	private: System::Void FinishBtn_Click(System::Object^ sender, System::EventArgs^ e) {
		SessionControls::getInstance().finishSession();
	}
	private: System::Void SessionControlPanel_Load(System::Object^ sender, System::EventArgs^ e) {
	}
	private: System::Void NextTrialBtn_click(System::Object^ sender, System::EventArgs^ e) {
		SessionControls::getInstance().nextTrial();
	}
	};
}
#endif // __SessionController__
