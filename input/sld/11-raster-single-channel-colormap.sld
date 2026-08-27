<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:se="http://www.opengis.net/se" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" version="1.1.0">
  <NamedLayer>
    <se:Name>Styling a DEM coverage</se:Name>
    <UserStyle>
      <se:Description>
        <se:Title>Styling a DEM coverage</se:Title>
        <se:Abstract>SLD/SE codec fixture: RasterSymbolizer/ChannelSelection/GrayChannel + ColorMap/Categorize with array [r,g,b] colors</se:Abstract>
      </se:Description>
      <se:FeatureTypeStyle>
        <se:CoverageName>Elevation</se:CoverageName>
        <se:Rule>
          <se:Name>Elevation</se:Name>
          <se:RasterSymbolizer>
            <se:ChannelSelection>
              <se:GrayChannel>
                <se:SourceChannelName>elevation</se:SourceChannelName>
              </se:GrayChannel>
            </se:ChannelSelection>
            <se:ColorMap>
              <se:Categorize fallbackValue="#608849">
                <se:LookupValue>Rasterdata</se:LookupValue>
                <se:Value>#608849</se:Value>
                <se:Threshold>900</se:Threshold>
                <se:Value>#e2dba7</se:Value>
                <se:Threshold>1300</se:Threshold>
                <se:Value>#fcc575</se:Value>
                <se:Threshold>1900</se:Threshold>
                <se:Value>#fea886</se:Value>
                <se:Threshold>2500</se:Threshold>
                <se:Value>#fafafa</se:Value>
              </se:Categorize>
            </se:ColorMap>
          </se:RasterSymbolizer>
        </se:Rule>
      </se:FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
