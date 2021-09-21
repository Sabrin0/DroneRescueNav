DroneRescueNav

# Build and Install
- Make sure AirSim is build and Unreal 4.26 is installed
- Clone the repo
- Double click on `DroneRescueNav.uproject`, if some modules are missing click *yes* in the new window
- Close UE4, then right click on `DroneRescueNav.uproject` and select **Generate Visual Studio project file**
- Open the generated `DroneRescueNav.sln` file with Visual Studio and make sure "DebugGame Editor" and "Win64" build configuration is the active build configuration.
- Press `F5` to `run`

# AirSim Settings

Please edit the `setting.json` file as follow (Inside the dir `..Documents\AirSim`):
```
{
  "SeeDocsAt": "https://github.com/Microsoft/AirSim/blob/master/docs/settings.md",
  "SettingsVersion": 1.2,
  "SimMode": "Multirotor",

  "DefaultSensors": {

    "Distance": {
      "SensorType": 5,
      "Enabled": true,
      "MinDistance": 0.2,
      "MaxDistance": 40,
      "X": 0,
      "Y": 0,
      "Z": -1,
      "Yaw": 0,
      "Pitch": 0,
      "Roll": 0,
      "DrawDebugPoints": true
    }
  }
}
```

# Trobleshooting 

> If the AirSim installation is fresh, i.e, hasn't been built before, make sure that you run `build.cmd` from the root directory once before copying `Unreal\Plugins` folder so that AirLib files are also included. If you have made some changes in the Blocks environment, make sure to run `update_to_git.bat` from `Unreal\Environments\Blocks` to update the files in Unreal\Plugins.

&nbsp;

> Install the [xBox 360 Controller emulator](https://www.x360ce.com/) depending on your current PC architecture. Open the exucatble, then configure and save before exit. Copy the 3 files (`.init`, `.exe` and `.dll`) inside the following dir `C:\Program Files\Epic Games\UE_426\Engine\Binaries\Win64`.

&nbsp;

> Update the `.NET 5.0` SDK