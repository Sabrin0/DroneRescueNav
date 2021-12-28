// Fill out your copyright notice in the Description page of Project Settings.
#include "savePose.h"
#include <fstream>
#include "Misc/FileHelper.h"
#include "HAL/PlatformFilemanager.h"
#include "Runtime/Engine/Public/EngineGlobals.h"

bool UsavePose::SavePoseTxt(FString SaveDirectory, FString FileName, TArray<FVector> Position, bool overwriting)
{
	SaveDirectory += "\\";
	SaveDirectory += FileName;

	if (!overwriting)
	{
		if (FPlatformFileManager::Get().GetPlatformFile().FileExists(*SaveDirectory))
		{
			return false;
		}
	}

	//FPlatformFileManager::Get().GetPlatformFile().DeleteFile(*SaveDirectory);

	// clear file
	/*
	std::ofstream ofs;
	ofs.open( *FileName, std::ofstream::out | std::ofstream::trunc);
	ofs.close();
	*/

	TArray<FString> pose;
	FString line = "";
	
	for (const FVector& line_position : Position)
	{
		//line += line_position.Printf(TEXT("%f"), line_position.);
		line += line.Printf(TEXT("%.3f %.3f %.3f"), line_position.X/100, line_position.Y/100, line_position.Z/100);
		line += LINE_TERMINATOR;
		pose.Add(line);
	}
	
	return FFileHelper::SaveStringArrayToFile(pose, *SaveDirectory, FFileHelper::EEncodingOptions::AutoDetect, &IFileManager::Get(), FILEWRITE_Append);
}
