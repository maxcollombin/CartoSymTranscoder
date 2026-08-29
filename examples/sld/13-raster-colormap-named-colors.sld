<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:se="http://www.opengis.net/se" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" version="1.1.0">
  <NamedLayer>
    <se:Name>Styling a hillshade coverage with named colors</se:Name>
    <UserStyle>
      <se:Description>
        <se:Title>Styling a hillshade coverage with named colors</se:Title>
        <se:Abstract>SLD/SE codec fixture: ColorMap/Categorize using CSS color names instead of hex</se:Abstract>
      </se:Description>
      <se:CoverageStyle>
        <se:CoverageName>Hillshade</se:CoverageName>
        <se:Rule>
          <se:Name>Hillshade</se:Name>
          <se:RasterSymbolizer>
            <se:ChannelSelection>
              <se:GrayChannel>
                <se:SourceChannelName>hillshade</se:SourceChannelName>
              </se:GrayChannel>
            </se:ChannelSelection>
            <se:ColorMap>
              <se:Categorize fallbackValue="black">
                <se:LookupValue>Rasterdata</se:LookupValue>
                <se:Value>black</se:Value>
                <se:Threshold>0.15</se:Threshold>
                <se:Value>gray</se:Value>
                <se:Threshold>0.35</se:Threshold>
                <se:Value>silver</se:Value>
                <se:Threshold>0.55</se:Threshold>
                <se:Value>white</se:Value>
              </se:Categorize>
            </se:ColorMap>
          </se:RasterSymbolizer>
        </se:Rule>
      </se:CoverageStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
