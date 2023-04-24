#include "SessionController.h"
#include <NIDAQmx.h>

using namespace System;
using namespace System::Windows::Forms;

void main() {
	Application::EnableVisualStyles();
	Application::SetCompatibleTextRenderingDefault(false);
	BSRunner::SessionController sessionController;
	Application::Run(% sessionController);
}
