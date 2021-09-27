// Fill out your copyright notice in the Description page of Project Settings.
#include "TextFileManager.h"
#include "Misc/FileHelper.h"
#include "HAL/PlatformFilemanager.h"
#include "Runtime/Engine/Public/EngineGlobals.h"

bool UTextFileManager::SaveArrayText(TArray<FString> time, FString SaveDirectory, FString FileName, TArray<FString> Location, TArray<FString> Orientation, TArray<FString> LinVel, TArray<FString> AngVel, bool AllowOverWriting)
// bool UTextFileManager::SaveArrayText(FString SaveDirectory, FString FileName, TArray<FString> SaveText, bool AllowOverWriting = true)
{
	//Set complete path
	SaveDirectory += "\\";
	SaveDirectory += FileName;

	if (!AllowOverWriting)
	{
		if (FPlatformFileManager::Get().GetPlatformFile().FileExists(*SaveDirectory))
		{
			return false;
		}
	}

	//FString FinalString = "";
	TArray<FString> Pose;
	FString Line = "";
	

	// for (const FString& data : SaveText) // old
	for (const FString& LineTime : time)
	{
		Line += "dt " + LineTime;
		for (const FString& LineLocation : Location)
		{
			/*
			//FinalString += Each;
			//GEngine->AddOnScreenDebugMessage(-1, 12.f, FColor::Red, FString::Printf(TEXT("%s"), *FinalString));
			//FinalString += LINE_TERMINATOR;
			//Pose.Add(Each);
			Line += data;
			Line += LINE_TERMINATOR;
			Pose.Add(Line);
			*/
			Line += "loc "+ LineLocation;
			for (const FString& LineOrientation : Orientation)
			{ 
				Line += "Or " + LineOrientation;
				for (const FString& LineLinVel : LinVel)
				{
					Line += "LV "+ LineLinVel;
					for (const FString& LineAngVel : AngVel)
					{
						Line += "Ang "+ LineAngVel;
					}
					
				}
				//Line += " Orientation" + LineOrientation;
				
			}
			Line += LINE_TERMINATOR;
			Pose.Add(Line);

		}
	}
	//return FFileHelper::SaveStringToFile(FinalString, *SaveDirectory);
	//return FFileHelper::SaveStringArrayToFile(Pose, *SaveDirectory);
	return FFileHelper::SaveStringArrayToFile(Pose, *SaveDirectory, FFileHelper::EEncodingOptions::AutoDetect, &IFileManager::Get(), FILEWRITE_Append);
}

