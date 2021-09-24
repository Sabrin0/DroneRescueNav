// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "TextFileManager.generated.h"

/**
 * 
 */
UCLASS()
class DRONERESCUENAV_API UTextFileManager : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

	// Callable from BluePrint
	UFUNCTION(BlueprintCallable, Category = "Custom", meta = (keywords = "Save"))

	// Function Declataration
	static bool SaveArrayText(FString SaveDirectory, FString FileName, TArray<FString> Location, TArray<FString> Orientation, bool AllowOverWriting);
	// static bool SaveArrayText(FString SaveDirectory, FString FileName, TArray<FString> SaveText, bool AllowOverWriting);
	
};
