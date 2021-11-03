// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "SPPlatformComponent.h"
#include "SPPlatformSpecificComponent.generated.h"

/**
 * 
 */
UCLASS(Blueprintable, BlueprintType, ClassGroup = (Custom), meta = (BlueprintSpawnableComponent))
class DRONERESCUENAV_API USPPlatformSpecificComponent : public USPPlatformComponent
{
	GENERATED_BODY()
		UFUNCTION(BlueprintCallable)
		bool SendFloatArray(TArray<float> data);
	
};
