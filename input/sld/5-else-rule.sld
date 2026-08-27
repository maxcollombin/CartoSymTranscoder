<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:se="http://www.opengis.net/se" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" version="1.1.0">
  <NamedLayer>
    <UserStyle>
      <se:Description>
        <se:Title>Styling with an else rule</se:Title>
        <se:Abstract>SLD/SE codec fixture: se:ElseFilter sibling rule</se:Abstract>
      </se:Description>
      <se:FeatureTypeStyle>
        <se:FeatureTypeName>Roads</se:FeatureTypeName>
        <se:Rule>
          <se:Name>Roads</se:Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>Class</ogc:PropertyName>
              <ogc:Literal>primary</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <se:LineSymbolizer>
            <se:Stroke>
              <se:SvgParameter name="stroke">#ff0000</se:SvgParameter>
              <se:SvgParameter name="stroke-width">3</se:SvgParameter>
              <se:SvgParameter name="stroke-opacity">1</se:SvgParameter>
            </se:Stroke>
          </se:LineSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:ElseFilter/>
          <se:LineSymbolizer>
            <se:Stroke>
              <se:SvgParameter name="stroke">#808080</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-opacity">1</se:SvgParameter>
            </se:Stroke>
          </se:LineSymbolizer>
        </se:Rule>
      </se:FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
