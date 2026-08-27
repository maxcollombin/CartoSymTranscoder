<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:se="http://www.opengis.net/se" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" version="1.1.0">
  <NamedLayer>
    <se:Name>FeatureTypeName round-trip</se:Name>
    <UserStyle>
      <se:Description>
        <se:Title>FeatureTypeName round-trip</se:Title>
        <se:Abstract>SLD/SE codec fixture: se:FeatureTypeName with no extra filter</se:Abstract>
      </se:Description>
      <se:FeatureTypeStyle>
        <se:FeatureTypeName>Buildings</se:FeatureTypeName>
        <se:Rule>
          <se:Name>Buildings</se:Name>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#f5f5dc</se:SvgParameter>
              <se:SvgParameter name="fill-opacity">1</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
      </se:FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
