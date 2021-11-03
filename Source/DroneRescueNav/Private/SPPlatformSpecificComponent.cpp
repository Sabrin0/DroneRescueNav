// Fill out your copyright notice in the Description page of Project Settings.


#include "SPPlatformSpecificComponent.h"

bool USPPlatformSpecificComponent::SendFloatArray(TArray<float> data) {
	FArrayWriter write;
	for (int i = 0; i < data.Num(); ++i) {
		write << data[i];
	}
	return Send(write);
}