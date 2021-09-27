// Fill out your copyright notice in the Description page of Project Settings.


#include "RightHanded.h"
#include "Math/Rotator.h"
#include "Math/Vector.h"

void  URightHanded::RightHandedT(const FVector Location, FVector& RLocation, const FRotator Orientation, FVector& ROrientation)

{	/* A Config
	RLocation.Set(Location.Y, Location.X, Location.Z);
	ROrientation.Set(Orientation.Pitch, -Orientation.Roll, -Orientation.Yaw);
	*/
	
	RLocation.Set(Location.X, -Location.Y, Location.Z);
	ROrientation.Set(-Orientation.Roll, -Orientation.Pitch, -Orientation.Yaw);

	//ROrientation.Set(Orientation.Pitch, -Orientation.Roll, -Orientation.Yaw);
	//return Location.Set(Location.Y, Location.X, Location.Z), ROrientation;
}
