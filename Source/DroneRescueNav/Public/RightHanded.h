// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "Math/Rotator.h"
#include "Math/Vector.h"
#include "RightHanded.generated.h"

UCLASS()
class DRONERESCUENAV_API URightHanded : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
	UFUNCTION(BlueprintCallable, Category = "Custom", meta = (keywords = "RightHanded"))

	static void RightHandedT(const FVector Location, FVector &RLocation, const FRotator Orientation, FVector &ROrientation);


};
