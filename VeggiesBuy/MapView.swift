//
//  MapView.swift
//  VeggiesBuy
//
//  Created by Gabriel Komarnicki on 5/5/2023.
//

import SwiftUI
import MapKit

struct Location: Identifiable {
    let id = UUID()
    let name: String
    let coordinate: CLLocationCoordinate2D
}

struct MapView: View {
    @State private var mapRegion = MKCoordinateRegion(center: CLLocationCoordinate2D(latitude: -34.4110, longitude: 150.8948), span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05))
    
    /*
    let locationsALDI = [
        Location(name: "ALDI Wollongong", coordinate: CLLocationCoordinate2D(latitude: -34.53, longitude: 150.90)),
        Location(name: "ALDI Fairy Meadow", coordinate: CLLocationCoordinate2D(latitude: -34.40, longitude: 150.90))
    ]
    
    let locationsColes = [
        Location(name: "Coles Wollongong", coordinate: CLLocationCoordinate2D(latitude: -34.43, longitude: 150.90)),
        Location(name: "Coles Fairy Meadow", coordinate: CLLocationCoordinate2D(latitude: -34.40, longitude: 150.90))
    ]
    
    let locationsWoolies = [
        Location(name: "Woolworths Wollongong", coordinate: CLLocationCoordinate2D(latitude: -34.43, longitude: 150.90)),
        Location(name: "Woolworths Fairy Meadow", coordinate: CLLocationCoordinate2D(latitude: -34.40, longitude: 150.90))
    ]*/
    
    let locations = [
        Location(name: "ALDI Wollongong", coordinate: CLLocationCoordinate2D(latitude: -34.4280, longitude: 150.8991)),
        Location(name: "ALDI Fairy Meadow", coordinate: CLLocationCoordinate2D(latitude: -34.3938, longitude: 150.8932)),
        Location(name: "Coles Wollongong", coordinate: CLLocationCoordinate2D(latitude: -34.4243, longitude: 150.8926)),
        Location(name: "Coles Fairy Meadow", coordinate: CLLocationCoordinate2D(latitude: -34.3947, longitude: 150.8932)),
        Location(name: "Woolworths Wollongong", coordinate: CLLocationCoordinate2D(latitude: -34.42703, longitude: 150.89611)),
        Location(name: "Woolworths Fairy Meadow", coordinate: CLLocationCoordinate2D(latitude: -34.3917, longitude: 150.8937))
    ]
    
    var body: some View {
        
        
        ZStack {
            //Color.themeBackground
                
            /*
            Map(coordinateRegion: $mapRegion, annotationItems: locationsWoolies) { location in MapAnnotation(coordinate: location.coordinate) {
                Circle()
                    .fill(.green)
                    .frame(width: 36, height: 36)
                    .shadow(radius: 2)
                }
            }*/
            
            Map(coordinateRegion: $mapRegion, annotationItems: locations) { location in MapAnnotation(coordinate: location.coordinate) {
                Circle()
                    .fill(.red)
                    .frame(width: 12, height: 12)
                    .shadow(radius: 2)
                    Text("Coles")
                }
            }
        }.ignoresSafeArea(.all, edges: .top)
    }
}

struct MapView_Previews: PreviewProvider {
    static var previews: some View {
        MapView()
    }
}
