#include "SessionController.h"
#include <NIDAQmx.h>

using namespace System;
using namespace System::Windows::Forms;

void main(int argc, char* argv[]) {
	Application::EnableVisualStyles();
	Application::SetCompatibleTextRenderingDefault(false);
	BSRunner::SessionController sessionController(argc, argv);
	Application::Run(% sessionController);
}
