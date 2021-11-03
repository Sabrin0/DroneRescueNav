// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Networking.h"
#include "Sockets.h"
#include "SocketSubsystem.h"

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "UUDPSender.generated.h"


UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class SPPLATFORMCOMMUNICATION_API UUDPSender : public UActorComponent
{
	GENERATED_BODY()

	TSharedPtr<FInternetAddr> RemoteAddr;
	FSocket* SenderSocket;
	bool IsUDP;

public:	
	// Sets default values for this component's properties
	UUDPSender();

	UFUNCTION(BlueprintCallable)
	bool StartUDPSender(const FString& YourChosenSocketName, const FString& TheIP, const int32 ThePort, bool UDP);


protected:
	// Called when the game starts
	virtual void BeginPlay() override;
	bool Send(FArrayWriter Writer);

public:	
	// Called every frame
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

		
};
