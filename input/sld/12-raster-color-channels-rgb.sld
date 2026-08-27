<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:se="http://www.opengis.net/se" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" version="1.1.0">
  <NamedLayer>
    <UserStyle>
      <se:Description>
        <se:Title>Styling a Sentinel-2 true-color coverage</se:Title>
        <se:Abstract>SLD/SE codec fixture: RasterSymbolizer/ChannelSelection with RedChannel/GreenChannel/BlueChannel, no alphaChannel</se:Abstract>
      </se:Description>
      <se:FeatureTypeStyle>
        <se:CoverageName>sentinel2-l2a</se:CoverageName>
        <se:Rule>
          <se:Name>TrueColor</se:Name>
          <se:RasterSymbolizer>
            <se:ChannelSelection>
              <se:RedChannel>
                <se:SourceChannelName>B04</se:SourceChannelName>
              </se:RedChannel>
              <se:GreenChannel>
                <se:SourceChannelName>B03</se:SourceChannelName>
              </se:GreenChannel>
              <se:BlueChannel>
                <se:SourceChannelName>B02</se:SourceChannelName>
              </se:BlueChannel>
            </se:ChannelSelection>
          </se:RasterSymbolizer>
        </se:Rule>
      </se:FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
