#pragma once
#ifndef __SessionController__
#define __SessionController__
#include "SessionControls.h"
#include <string>

namespace BSRunner {
	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;

	public ref class SessionController : public System::Windows::Forms::Form {
	public:
		SessionController(void) {
			InitializeComponent();
		}

	protected:
		~SessionController() {
			if (components) {
				delete components;
			}
		}

	private:
		System::ComponentModel::Container^ components;
		System::Windows::Forms::Button^ StartBtn;
		System::Windows::Forms::Button^ PauseBtn;
		System::Windows::Forms::Button^ ResumeBtn;
		System::Windows::Forms::Button^ RewardBtn;
		System::Windows::Forms::Button^ FinishBtn;
		System::Windows::Forms::Panel^ panel1;

#pragma region Windows Form Designer generated code
		void InitializeComponent(void) {
			this->StartBtn = (gcnew System::Windows::Forms::Button());
			this->PauseBtn = (gcnew System::Windows::Forms::Button());
			this->ResumeBtn = (gcnew System::Windows::Forms::Button());
			this->RewardBtn = (gcnew System::Windows::Forms::Button());
			this->FinishBtn = (gcnew System::Windows::Forms::Button());
			this->panel1 = (gcnew System::Windows::Forms::Panel());
			this->panel1->SuspendLayout();
			this->SuspendLayout();
			// 
			// StartBtn
			// 
			this->StartBtn->Anchor = System::Windows::Forms::AnchorStyles::None;
			this->StartBtn->Location = System::Drawing::Point(21, 14);
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
			this->PauseBtn->Location = System::Drawing::Point(21, 66);
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
			this->ResumeBtn->Location = System::Drawing::Point(128, 66);
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
			this->RewardBtn->Location = System::Drawing::Point(21, 120);
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
			this->FinishBtn->Location = System::Drawing::Point(21, 176);
			this->FinishBtn->Name = L"FinishBtn";
			this->FinishBtn->Size = System::Drawing::Size(199, 35);
			this->FinishBtn->TabIndex = 4;
			this->FinishBtn->Text = L"Finish";
			this->FinishBtn->UseVisualStyleBackColor = true;
			this->FinishBtn->Click += gcnew System::EventHandler(this, &SessionController::FinishBtn_Click);
			// 
			// panel1
			// 
			this->panel1->Anchor = static_cast<System::Windows::Forms::AnchorStyles>((((System::Windows::Forms::AnchorStyles::Top | System::Windows::Forms::AnchorStyles::Bottom)
				| System::Windows::Forms::AnchorStyles::Left)
				| System::Windows::Forms::AnchorStyles::Right));
			this->panel1->Controls->Add(this->RewardBtn);
			this->panel1->Controls->Add(this->StartBtn);
			this->panel1->Controls->Add(this->ResumeBtn);
			this->panel1->Controls->Add(this->FinishBtn);
			this->panel1->Controls->Add(this->PauseBtn);
			this->panel1->Location = System::Drawing::Point(12, 12);
			this->panel1->Name = L"panel1";
			this->panel1->Size = System::Drawing::Size(235, 231);
			this->panel1->TabIndex = 5;
			// 
			// SessionController
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(6, 13);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(257, 253);
			this->Controls->Add(this->panel1);
			this->Name = L"SessionController";
			this->Text = L"Control Board";
			this->Load += gcnew System::EventHandler(this, &SessionController::SessionControlPanel_Load);
			this->panel1->ResumeLayout(false);
			this->ResumeLayout(false);

		}
#pragma endregion
	private: System::Void PauseBtn_Click(System::Object^ sender, System::EventArgs^ e) {
		SessionControls::getInstance().pauseSession();
	}
	private: System::Void StartBtn_Click(System::Object^ sender, System::EventArgs^ e) {
		SessionControls::getInstance().startSession();
	}
	private: System::Void ResumeBtn_Click(System::Object^ sender, System::EventArgs^ e) {
		SessionControls::getInstance().resumeSession();
	}
	private: System::Void RewardBtn_Click(System::Object^ sender, System::EventArgs^ e) {
		MessageBox::Show("Reward was given");
	}
	private: System::Void FinishBtn_Click(System::Object^ sender, System::EventArgs^ e) {
		SessionControls::getInstance().finishSession();
	}
	private: System::Void SessionControlPanel_Load(System::Object^ sender, System::EventArgs^ e) {
	}
	};
}
#endif // __SessionController__
