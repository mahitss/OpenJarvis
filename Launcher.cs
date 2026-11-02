using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Runtime.InteropServices;

[assembly: AssemblyTitle("J.A.R.V.I.S. Personal AI")]
[assembly: AssemblyDescription("J.A.R.V.I.S. Autonomous Desktop & Voice Assistant")]
[assembly: AssemblyProduct("J.A.R.V.I.S.")]
[assembly: AssemblyCompany("J.A.R.V.I.S.")]
[assembly: AssemblyVersion("1.0.0.0")]
[assembly: AssemblyFileVersion("1.0.0.0")]

namespace OpenJarvisLauncher
{
    class Program
    {
        [DllImport("user32.dll")]
        private static extern bool SetProcessDPIAware();

        static void Main(string[] args)
        {
            try
            {
                SetProcessDPIAware();
                string appDir = AppDomain.CurrentDomain.BaseDirectory;
                string venvPython = Path.Combine(appDir, ".venv", "Scripts", "python.exe");
                string launchScript = Path.Combine(appDir, "launch_jarvis.py");

                if (!File.Exists(venvPython))
                {
                    venvPython = "python.exe";
                }

                ProcessStartInfo psi = new ProcessStartInfo();
                psi.FileName = venvPython;
                psi.Arguments = "\"" + launchScript + "\"";
                psi.WorkingDirectory = appDir;
                psi.UseShellExecute = false;
                psi.CreateNoWindow = true;

                Process.Start(psi);
            }
            catch (Exception ex)
            {
                // In case of error, show a message box
                System.Windows.Forms.MessageBox.Show(
                    "Failed to launch J.A.R.V.I.S.: " + ex.Message,
                    "J.A.R.V.I.S. Error",
                    System.Windows.Forms.MessageBoxButtons.OK,
                    System.Windows.Forms.MessageBoxIcon.Error
                );
            }
        }
    }
}
