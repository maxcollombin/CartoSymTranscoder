<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:se="http://www.opengis.net/se" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" version="1.1.0">
  <NamedLayer>
    <se:Name>Filter breadth</se:Name>
    <UserStyle>
      <se:Description>
        <se:Title>Filter breadth</se:Title>
        <se:Abstract>SLD/SE codec fixture: Between, Like, Not(IsNull), And/Or of comparisons</se:Abstract>
      </se:Description>
      <se:FeatureTypeStyle>
        <se:Rule>
          <se:Name>Amenities</se:Name>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsBetween>
                <ogc:PropertyName>Population</ogc:PropertyName>
                <ogc:LowerBoundary>
                  <ogc:Literal>1000</ogc:Literal>
                </ogc:LowerBoundary>
                <ogc:UpperBoundary>
                  <ogc:Literal>5000</ogc:Literal>
                </ogc:UpperBoundary>
              </ogc:PropertyIsBetween>
              <ogc:PropertyIsLike wildCard="%" singleChar="_" escapeChar="\">
                <ogc:PropertyName>Name</ogc:PropertyName>
                <ogc:Literal>%park%</ogc:Literal>
              </ogc:PropertyIsLike>
              <ogc:Not>
                <ogc:PropertyIsNull>
                  <ogc:PropertyName>Name</ogc:PropertyName>
                </ogc:PropertyIsNull>
              </ogc:Not>
              <ogc:Or>
                <ogc:PropertyIsLessThan>
                  <ogc:PropertyName>Population</ogc:PropertyName>
                  <ogc:Literal>100</ogc:Literal>
                </ogc:PropertyIsLessThan>
                <ogc:PropertyIsGreaterThan>
                  <ogc:PropertyName>Population</ogc:PropertyName>
                  <ogc:Literal>100000</ogc:Literal>
                </ogc:PropertyIsGreaterThan>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#ffff00</se:SvgParameter>
              <se:SvgParameter name="fill-opacity">0.7</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
      </se:FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
