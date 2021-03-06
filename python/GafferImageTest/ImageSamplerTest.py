##########################################################################
#
#  Copyright (c) 2013, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import imath

import IECore
import IECoreImage

import Gaffer
import GafferTest
import GafferImage
import GafferImageTest

class ImageSamplerTest( GafferImageTest.ImageTestCase ) :

	def test( self ) :

		dataWindow = imath.Box2i( imath.V2i( 0 ), imath.V2i( 74 ) )
		image = IECoreImage.ImagePrimitive( dataWindow, dataWindow )
		red = IECore.FloatVectorData()
		green = IECore.FloatVectorData()
		blue = IECore.FloatVectorData()
		image["R"] = red
		image["G"] = green
		image["B"] = blue
		for y in range( 0, 75 ) :
			for x in range( 0, 75 ) :
				red.append( x )
				green.append( y )
				blue.append( 0 )

		imageNode = GafferImage.ObjectToImage()
		imageNode["object"].setValue( image )

		sampler = GafferImage.ImageSampler()
		sampler["image"].setInput( imageNode["out"] )

		hashes = set()
		for x in range( 0, 75 ) :
			for y in range( 0, 75 ) :
				sampler["pixel"].setValue( imath.V2f( x + 0.5, y + 0.5 ) )
				# the flip in y is necessary as gaffer image coordinates run bottom->top and
				# cortex image coordinates run top->bottom.
				self.assertEqual( sampler["color"].getValue(), imath.Color4f( x, 74 - y, 0, 0 ) )
				hashes.add( str( sampler["color"].hash() ) )

		self.assertEqual( len( hashes ), 75 * 75 )

	def testChannelsPlug( self ) :

		constant = GafferImage.Constant()
		constant["layer"].setValue( "diffuse" )
		constant["color"].setValue( imath.Color4f( 1, 0.5, 0.25, 1 ) )

		sampler = GafferImage.ImageSampler()
		sampler["image"].setInput( constant["out"] )
		sampler["pixel"].setValue( imath.V2f( 10.5 ) )
		self.assertEqual( sampler["color"].getValue(), imath.Color4f( 0, 0, 0, 0 ) )

		sampler["channels"].setValue( IECore.StringVectorData( [ "diffuse.R", "diffuse.G", "diffuse.B", "diffuse.A" ] ) )
		self.assertEqual( sampler["color"].getValue(), imath.Color4f( 1, 0.5, 0.25, 1 ) )

if __name__ == "__main__":
	unittest.main()
