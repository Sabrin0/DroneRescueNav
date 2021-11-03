// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "UUDPSender.h"
#include "SPPlatformUDPSender.generated.h"

/**
 * 
 */
UCLASS(Blueprintable, BlueprintType, ClassGroup = (Custom), meta = (BlueprintSpawnableComponent))
class SPPLATFORMCOMMUNICATION_API USPPlatformUDPSender : public UUDPSender
{
	GENERATED_BODY()
	
		UFUNCTION(BlueprintCallable)
		bool SendFloatArray(TArray<float> data);
};
