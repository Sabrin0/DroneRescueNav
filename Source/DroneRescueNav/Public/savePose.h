// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "savePose.generated.h"


/**
 *	Save drone pose during navigation
 */
UCLASS()
class DRONERESCUENAV_API UsavePose : public UBlueprintFunctionLibrary
{
		GENERATED_BODY()
		// Callable from BP
		UFUNCTION(BlueprintCallable, Category = "Custom", meta = (keywords = "save only pose"))

		static bool SavePoseTxt(FString SaveDirectory, FString FileName, TArray<FVector> Position, bool overwriting);
};
