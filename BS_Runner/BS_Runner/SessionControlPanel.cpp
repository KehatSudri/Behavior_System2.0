#include "SessionControlPanel.h"
#include <NIDAQmx.h>

using namespace System;
using namespace System::Windows::Forms;

void main() {
	Application::EnableVisualStyles();
	Application::SetCompatibleTextRenderingDefault(false);
	BSRunner::SessionControlPanel form;
	Application::Run(% form);
}
