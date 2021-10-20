// Fill out your copyright notice in the Description page of Project Settings.


#include "RightHanded.h"
#include "Misc/FileHelper.h"
#include "Math/Rotator.h"
#include "Math/Vector.h"
#include "Math/UnrealMathUtility.h"


// void  URightHanded::RightHandedT(const FVector Location, FVector& RLocation, const FRotator Orientation, FVector& ROrientation)
void  URightHanded::RightHandedT(const FVector Location, FString& RLocation, const FRotator Orientation, FString& ROrientation, FVector LinVel, FString& RLinVel, FVector AngVel, FString& RAngVel)

{	/* A Config
	RLocation.Set(Location.Y, Location.X, Location.Z);
	ROrientation.Set(Orientation.Pitch, -Orientation.Roll, -Orientation.Yaw);
	*/
	
	// Change of coordinate
	/*RLocation.Set(Location.X, -Location.Y, Location.Z);
	RLocation.ToString();
	ROrientation.Set(-Orientation.Roll, -Orientation.Pitch, -Orientation.Yaw);
	ROrientation.ToString();
	*/
	FVector RLoc = FVector(Location.X, -Location.Y, Location.Z);
	FVector RRot = FVector(-Orientation.Roll, -Orientation.Pitch, -Orientation.Yaw);
	LinVel.Set(LinVel.X, -LinVel.Y, LinVel.Z);
	AngVel.Set(-AngVel.X, -AngVel.Y, -AngVel.Z);
	
	RLocation = RLocation.Printf(TEXT(" %f %f %f"), RLoc.X, RLoc.Y, RLoc.Z);
	ROrientation = ROrientation.Printf(TEXT(" %f %f %f"), RRot.X, RRot.Y, RRot.Z);
	RLinVel = RLinVel.Printf(TEXT(" %f %f %f"), LinVel.X, LinVel.Y, LinVel.Z);
	RAngVel = RAngVel.Printf(TEXT(" %f %f %f"), AngVel.X, AngVel.Y, AngVel.Z);

	//ROrientation =RRot.ToCompactString();

	//ROrientation.Set(Orientation.Pitch, -Orientation.Roll, -Orientation.Yaw);
	//return Location.Set(Location.Y, Location.X, Location.Z), ROrientation;
}
