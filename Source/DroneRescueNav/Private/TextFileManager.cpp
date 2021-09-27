// Fill out your copyright notice in the Description page of Project Settings.
#include "TextFileManager.h"
#include "Misc/FileHelper.h"
#include "HAL/PlatformFilemanager.h"
#include "Runtime/Engine/Public/EngineGlobals.h"

bool UTextFileManager::SaveArrayText(FString SaveDirectory, FString FileName, TArray<FString> Location, TArray<FString> Orientation, bool AllowOverWriting = true)
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
		Line += LineLocation;
		for (const FString& LineOrientation : Orientation)
		{
			//Line += " Orientation" + LineOrientation;
			Line += LineOrientation;
		}

		Line += LINE_TERMINATOR;
		Pose.Add(Line);

	}

	//return FFileHelper::SaveStringToFile(FinalString, *SaveDirectory);
	//return FFileHelper::SaveStringArrayToFile(Pose, *SaveDirectory);
	return FFileHelper::SaveStringArrayToFile(Pose, *SaveDirectory, FFileHelper::EEncodingOptions::AutoDetect, &IFileManager::Get(), FILEWRITE_Append);
}

