from __future__ import annotations #fix issues with forward references in type hints (DelftBlue PVbatch is old)
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from base import PostStage

class ProbesPlotterAirbox(PostStage): #Class object that inherits from the PostStage base class, responsible for generating pressure plots inside sidepods from OpenFOAM simulation data
    name = "Airbox_probes" #this name needs to match the name in the config.yaml!
    
    def run(self) -> list[Path]:
        #cfg = self.config.get("probesPressure", {}) # retrieves the configuration settings for the probes pressure plotter from the overall configuration dictionary, using "probesPressure" as the key, and defaults to an empty dictionary if no specific settings are found
        file_path_p = self.case_dir / self.config.get("file_p", "postProcessing/probes_airbox/0/p") # constructs the file path to the probes data file by combining the case directory with the relative path specified in the configuration, defaulting to "postProcessing/probes/0/probes.dat" if no specific file path is provided in the configuration
        file_path_U = self.case_dir / self.config.get("file_U", "postProcessing/probes_airbox/0/U") # constructs the file path to the velocity probes data file by combining the case directory with the relative path specified in the configuration, defaulting to "postProcessing/probes/0/probes.dat" if no specific file path is provided in the configuration
        # Read the file (whitespace-delimited, skip comment lines)
        df = pd.read_csv(
            file_path_p,
            sep=r"\s+",
            comment="#",
            header=None,
            engine="python"
        )
        df_U = pd.read_csv(
            file_path_U,
            sep=r"\s+",
            comment="#",
            header=None,
            engine="python"
        )
        # first 14 rows are commented, left column is time and the following 13 columns are the probes from the pressure rake, we want to plot pressure vs time
        df.columns = ["Time", "0", "1", "2","3","4","5","6","7","8","9","10","11","12"] # Assign column names to the DataFrame for easier access
        output_paths = []
        # calculate averaged pressure across all probes at each time step
        probe_cols = ["0","1","2","3","4","5","6","7","8","9","10","11","12"]
        df = df[df["Time"] >= 100] # Filter out rows where Time is less than 100 to focus on the steady-state portion of the simulation
        df["Pressure"] = df.loc[:, "0":"12"].mean(axis=1)
        # Plot pressure vs time
        plt.figure(figsize=(6, 4))
        plt.plot(df["Time"], df["Pressure"], color="#4C72B0",linewidth=2.0, label="Mean")
        plt.title("Averaged Airbox Rake Pressure per Iteration")
        plt.xlabel("Iterations [-]")
        plt.ylabel("Pressure  [Pa]")
        plt.grid(axis="y", linestyle="-", alpha=0.5)

        # Save figure
        plt.tight_layout()
        output_path = self.out_dir / "airbox_pressure_time.png"
        plt.savefig(output_path, dpi=150)
        plt.close()  # Close the figure to free memory
        self.log(f"Saved Airbox pressure plot to {output_path}")
        output_paths.append(output_path)

        # Plot all pressure probes:
        cmap = plt.get_cmap("tab20", len(probe_cols))
        plt.figure(figsize=(6, 4))
        for i, col in enumerate(probe_cols):
            plt.plot(df["Time"], df[col], color=cmap(i), linewidth=1.2, label=f"Probe {col}")
        plt.title("Airbox Rake Pressure per Probe")
        plt.xlabel("Iterations [-]")
        plt.ylabel("Pressure  [Pa]")
        plt.grid(axis="y", linestyle="-", alpha=0.5)
        plt.legend(fontsize=7, ncol=2, loc="upper right")
        plt.tight_layout()
        output_path = self.out_dir / "airbox_pressure_all_probes.png"
        plt.savefig(output_path, dpi=150)
        plt.close() # close the figure to free memory
        self.log(f"Saved Airbox pressure all-probes plot to {output_path}")
        output_paths.append(output_path)

        #Velocity plot (x direction only, as the rake is aligned with the flow)
        x_col_indices = [1 + 3*i for i in range(13)]  # Takes only Ux compoenntn
        df_U = df_U.iloc[:, [0] + x_col_indices].copy() # Keep only the time column and the x-velocity columns, and make a copy
        df_U.columns = ["Time", "0", "1", "2","3","4","5","6","7","8","9","10","11","12"]
        df_U = df_U[df_U["Time"] >= 100]  # filter here too
        # Strip the leading "(" from the x-component values
        for col in probe_cols:
            df_U[col] = df_U[col].astype(str).str.lstrip("(").astype(float)
        df_U["Velocity"] = df_U.loc[:, "0":"12"].mean(axis=1)
        # Plot velocity vs time
        plt.figure(figsize=(6, 4))
        plt.plot(df_U["Time"], df_U["Velocity"], color="#4C72B0",linewidth=2.0, label="Mean")
        plt.title("Averaged Airbox Rake Velocity per Iteration")
        plt.xlabel("Iterations [-]")
        plt.ylabel("Velocity  [m/s]")
        plt.grid(axis="y", linestyle="-", alpha=0.5)

        # Save figure
        plt.tight_layout()
        output_path = self.out_dir / "airbox_velocity_time.png"
        plt.savefig(output_path, dpi=150)
        plt.close()  # Close the figure to free memory
        self.log(f"Saved Airbox velocity plot to {output_path}")
        output_paths.append(output_path)

        # Plot all velocity probes:
        cmap = plt.get_cmap("tab20", len(probe_cols))
        plt.figure(figsize=(6, 4))
        for i, col in enumerate(probe_cols):
            plt.plot(df_U["Time"], df_U[col], color=cmap(i), linewidth=1.2, label=f"Probe {col}")
        plt.title("Airbox Rake Velocity per Probe")
        plt.xlabel("Iterations [-]")
        plt.ylabel("Velocity  [m/s]")
        plt.grid(axis="y", linestyle="-", alpha=0.5)
        plt.legend(fontsize=7, ncol=2, loc="upper right")
        plt.tight_layout()
        output_path = self.out_dir / "airbox_velocity_all_probes.png"
        plt.savefig(output_path, dpi=150)
        plt.close() # close the figure to free memory
        self.log(f"Saved Sidepod velocity all-probes plot to {output_path}")
        output_paths.append(output_path)

        return output_paths


# ----------------- Sidepod        
    
class ProbesPlotterSidepod(PostStage): #Class object that inherits from the PostStage base class, responsible for generating pressure plots inside sidepods from OpenFOAM simulation data
    name = "Sidepod_probes" #this name needs to match the name in the config.yaml!
    
    def run(self) -> list[Path]:
        cfg = self.config.get("probesPressure", {}) # retrieves the configuration settings for the probes pressure plotter from the overall configuration dictionary, using "probesPressure" as the key, and defaults to an empty dictionary if no specific settings are found
        file_path_p = self.case_dir / cfg.get("file_p", "postProcessing/probes_sidepod/0/p") # constructs the file path to the probes data file by combining the case directory with the relative path specified in the configuration, defaulting to "postProcessing/probes/0/probes.dat" if no specific file path is provided in the configuration
        file_path_U = self.case_dir / cfg.get("file_U", "postProcessing/probes_sidepod/0/U") # constructs the file path to the velocity probes data file by combining the case directory with the relative path specified in the configuration, defaulting to "postProcessing/probes/0/probes.dat" if no specific file path is provided in the configuration
        # Read the file (whitespace-delimited, skip comment lines)
        df = pd.read_csv(
            file_path_p,
            sep=r"\s+",
            comment="#",
            header=None,
            engine="python"
        )
        df_U = pd.read_csv(
            file_path_U,
            sep=r"\s+",
            comment="#",
            header=None,
            engine="python"
        )
        # first 14 rows are commented, left column is time and the following 18 columns are the probes from the pressure rake, we want to plot pressure vs time
        df.columns = ["Time", "0", "1", "2","3","4","5","6","7","8","9","10","11","12", "13", "14", "15", "16", "17"] # Assign column names to the DataFrame for easier access
        output_paths = []
        # calculate averaged pressure across all probes at each time step
        probe_cols = ["0","1","2","3","4","5","6","7","8","9","10","11","12", "13", "14", "15", "16", "17"]
        df = df[df["Time"] >= 100] # Filter out rows where Time is less than 100 to focus on the steady-state portion of the simulation
        df["Pressure"] = df.loc[:, "0":"17"].mean(axis=1)
        # Plot pressure vs time
        plt.figure(figsize=(6, 4))
        plt.plot(df["Time"], df["Pressure"], color="#4C72B0",linewidth=2.0, label="Mean")
        plt.title("Averaged Sidepod Rake Pressure per Iteration")
        plt.xlabel("Iterations [-]")
        plt.ylabel("Pressure  [Pa]")
        plt.grid(axis="y", linestyle="-", alpha=0.5)

        # Save figure
        plt.tight_layout()
        output_path = self.out_dir / "sidepod_pressure_time.png"
        plt.savefig(output_path, dpi=150)
        plt.close()  # Close the figure to free memory
        self.log(f"Saved Sidepod pressure plot to {output_path}")
        output_paths.append(output_path)

        # Plot all pressure probes:
        cmap = plt.get_cmap("tab20", len(probe_cols))
        plt.figure(figsize=(6, 4))
        for i, col in enumerate(probe_cols):
            plt.plot(df["Time"], df[col], color=cmap(i), linewidth=1.2, label=f"Probe {col}")
        plt.title("Sidepod Rake Pressure per Probe")
        plt.xlabel("Iterations [-]")
        plt.ylabel("Pressure  [Pa]")
        plt.grid(axis="y", linestyle="-", alpha=0.5)
        plt.legend(fontsize=7, ncol=2, loc="upper right")
        plt.tight_layout()
        output_path = self.out_dir / "sidepod_pressure_all_probes.png"
        plt.savefig(output_path, dpi=150)
        plt.close() # close the figure to free memory
        self.log(f"Saved Sidepod pressure all-probes plot to {output_path}")
        output_paths.append(output_path)

        #Velocity plot (x direction only, as the rake is aligned with the flow)
        x_col_indices = [1 + 3*i for i in range(18)]  # Takes only Ux compoenntn
        df_U = df_U.iloc[:, [0] + x_col_indices].copy() # Keep only the time column and the x-velocity columns, and make a copy
        df_U.columns = ["Time", "0", "1", "2","3","4","5","6","7","8","9","10","11","12", "13", "14", "15", "16", "17"]
        df_U = df_U[df_U["Time"] >= 100]  # filter here too
        # Strip the leading "(" from the x-component values
        for col in probe_cols:
            df_U[col] = df_U[col].astype(str).str.lstrip("(").astype(float)
        df_U["Velocity"] = df_U.loc[:, "0":"17"].mean(axis=1)
        # Plot velocity vs time
        plt.figure(figsize=(6, 4))
        plt.plot(df_U["Time"], df_U["Velocity"], color="#4C72B0",linewidth=2.0, label="Mean")
        plt.title("Averaged Sidepod Rake Velocity per Iteration")
        plt.xlabel("Iterations [-]")
        plt.ylabel("Velocity  [m/s]")
        plt.grid(axis="y", linestyle="-", alpha=0.5)

        # Save figure
        plt.tight_layout()
        output_path = self.out_dir / "sidepod_velocity_time.png"
        plt.savefig(output_path, dpi=150)
        plt.close()  # Close the figure to free memory
        self.log(f"Saved Sidepod velocity plot to {output_path}")
        output_paths.append(output_path)

        # Plot all velocity probes:
        cmap = plt.get_cmap("tab20", len(probe_cols))
        plt.figure(figsize=(6, 4))
        for i, col in enumerate(probe_cols):
            plt.plot(df_U["Time"], df_U[col], color=cmap(i), linewidth=1.2, label=f"Probe {col}")
        plt.title("Sidepod Rake Velocity per Probe")
        plt.xlabel("Iterations [-]")
        plt.ylabel("Velocity  [m/s]")
        plt.grid(axis="y", linestyle="-", alpha=0.5)
        plt.legend(fontsize=7, ncol=2, loc="upper right")
        plt.tight_layout()
        output_path = self.out_dir / "sidepod_velocity_all_probes.png"
        plt.savefig(output_path, dpi=150)
        plt.close() # close the figure to free memory
        self.log(f"Saved Sidepod velocity all-probes plot to {output_path}")
        output_paths.append(output_path)

        return output_paths