<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:se="http://www.opengis.net/se" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" version="1.1.0">
  <NamedLayer>
    <UserStyle>
      <se:Description>
        <se:Title>Out-of-scope raster styling</se:Title>
        <se:Abstract>SLD/SE codec fixture: se:RasterSymbolizer/se:ContrastEnhancement must raise NotImplementedError (Part-4/out-of-scope construct, see mapping-issues issue #26)</se:Abstract>
      </se:Description>
      <se:FeatureTypeStyle>
        <se:CoverageName>Elevation</se:CoverageName>
        <se:Rule>
          <se:Name>Hillshade</se:Name>
          <se:RasterSymbolizer>
            <se:ContrastEnhancement>
              <se:Normalize/>
            </se:ContrastEnhancement>
          </se:RasterSymbolizer>
        </se:Rule>
      </se:FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
