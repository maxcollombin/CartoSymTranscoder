<?xml version='1.0' encoding='UTF-8'?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:se="http://www.opengis.net/se" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1.0">
  <NamedLayer>
    <se:Name>Styling with an image marker</se:Name>
    <UserStyle>
      <se:Description>
        <se:Title>Styling with an image marker</se:Title>
        <se:Abstract>SLD/SE codec fixture: PointSymbolizer/Graphic/ExternalGraphic/OnlineResource + AnchorPoint (from hotSpot)</se:Abstract>
      </se:Description>
      <se:FeatureTypeStyle>
        <se:Rule>
          <se:Name>ParkingIcon</se:Name>
          <ogc:Filter>
            <ogc:PropertyIsEqualTo>
              <ogc:PropertyName>FunctionCode</ogc:PropertyName>
              <ogc:Literal>parking</ogc:Literal>
            </ogc:PropertyIsEqualTo>
          </ogc:Filter>
          <se:PointSymbolizer>
            <se:Graphic>
              <se:ExternalGraphic>
                <se:OnlineResource xlink:type="simple" xlink:href="http://example.com/parkingIcon.png"/>
                <se:Format>image/png</se:Format>
              </se:ExternalGraphic>
            </se:Graphic>
            <se:AnchorPoint>
              <se:AnchorPointX>0.5</se:AnchorPointX>
              <se:AnchorPointY>0.5</se:AnchorPointY>
            </se:AnchorPoint>
          </se:PointSymbolizer>
        </se:Rule>
      </se:FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
