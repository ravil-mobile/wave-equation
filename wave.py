import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import math


def main():


    # Domain settings
    NumberOfElements= 100
    Max = 0.1
    Min = 0.0
    SpatialStep = abs( Max - Min ) / ( NumberOfElements - 1 )
    x = np.linspace( Min, Max, NumberOfElements )


    # Geometrical properties of the string
    Length = abs(Max - Min)
    Diameter = 1.0e-3
    CrossSectionArea = math.pi * Diameter**2 / 4.0


    # Material properties
    ElasticityCoefficient = 200000 * 10e6
    Elasticity = ( ElasticityCoefficient * CrossSectionArea ) / ( Length )
    Density = 7800
    MaterialProperies = ( Elasticity ) / ( Density )


    # Damping properties
    DampingCoefficient = 550.0


    # Time settings
    TimeStart = 0.0
    TimeEnd = 1.0
    TimeStep = 2.0e-5


    # Initial Conditions
    PriviousDisplacement = []
    Amplitude = 5.0e-3
    for i in range( 0, len( x ) ):
        #PriviousDisplacement.append( ( Amplitude * 4.0 / Max**2 ) * x[i] * (x[i] - Max )  )
        PriviousDisplacement.append( x[i]**2 * math.sin( math.pi * x[i] / Max ) )

    # Boundary Conditions
    PriviousDisplacement[0] = 0;
    PriviousDisplacement[-1] = 0;


    # Compute the first timestep
    CurrentTime = TimeStep
    CurrentDisplacement = computeFirstStep( PriviousDisplacement, \
                                            TimeStep, \
                                            SpatialStep, \
                                            MaterialProperies, \
                                            DampingCoefficient )


    # Run the main loop
    Temp = 0
    CounterFrame = 1;
    while( CurrentTime < TimeEnd ):

        # Update the screen
        depictPlot( x, CurrentDisplacement )
        #plt.savefig( 'Frame%03d.png' % CounterFrame )

        # Make computation
        Temp = computeNextStep( CurrentDisplacement, \
                                PriviousDisplacement, \
                                TimeStep, \
                                SpatialStep, \
                                MaterialProperies, \
                                DampingCoefficient )

        PriviousDisplacement = CurrentDisplacement
        CurrentDisplacement = Temp

        # Increment the Current simulation time
        CurrentTime += TimeStep
        CounterFrame += 1





def computeFirstStep( u, TimeStep, SpatialStep, MaterialProperties, DampingCoefficient ):

    NewDisplacement = [ 0.0 ];
    Coefficient = ( MaterialProperties * TimeStep \
                    / ( 2.0 * SpatialStep**2 * ( 1.0 + DampingCoefficient ) ) )

    Temp = 0;
    for i in range( 1, len(u) - 1 ):
        Temp = Coefficient * ( u[ i - 1 ] - 2 * u[ i ] + u[ i + 1 ] ) + u[ i ]
        NewDisplacement.append( Temp )

    NewDisplacement.append( 0.0 )
    return NewDisplacement


def computeNextStep( uCurrent, \
                     uPrivious, \
                     TimeStep, \
                     SpatialStep, \
                     MaterialProperties, \
                     DampingCoefficient ):

    NewDisplacement = [ 0.0 ];

    Coeff = ( 1.0 + TimeStep * DampingCoefficient )

    CoeffOne = ( ( MaterialProperties * TimeStep**2 ) / ( ( SpatialStep**2 * Coeff ) ) )
    CoeffTwo = 2.0 / ( Coeff )
    CoeffTree = (( DampingCoefficient * TimeStep ) / Coeff )
    CoeffFour = (( 1.0 ) / ( Coeff ))

    Temp = 0;
    for i in range( 1, len(uCurrent) - 1 ):
        Temp = CoeffOne \
               * ( uCurrent[ i - 1 ] - 2 * uCurrent[ i ] + uCurrent[ i + 1 ] ) \
               + CoeffTwo * uCurrent[ i ] \
               + CoeffTree * uCurrent[ i ] \
               - CoeffFour * uPrivious[ i ]
        NewDisplacement.append( Temp )

    NewDisplacement.append( 0.0 )
    return NewDisplacement



def depictPlot( x, CurrentDisplacement ):

    # Clean figure
    plt.clf()

    # Set up plot
    plt.plot( x, CurrentDisplacement )

    # Adjast axis
    plt.ylim(-0.02, 0.02)

    # Draw the plot
    plt.draw()

    # Make pause
    plt.pause(0.01)

main()