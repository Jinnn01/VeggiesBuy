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

struct VegetableMap: Hashable, Codable {
    //let sname: String
    let vname: String
    let price: Float
    //let unit: String
    //let image: String
}

/*
struct Supermarket: Hashable, Codable {
    let sname: String
    let slatitude: String
    let slongitude: String
}*/

// iosacademy tutorial
class ViewMapModel: ObservableObject {
    @Published var vegetablesMap: [VegetableMap] = []
    //@State private var supermarkets: [Supermarket] = []
    
    func fetch() {
        //guard let url = URL(string: "https://iosacademy.io/api/v1/courses/index.php") else {
            //return
        guard let url = URL(string: "http://localhost:5005/item") else {
            return
        }
        
        let task = URLSession.shared.dataTask(with: url) { [weak self] data, _,
            error in
            guard let data = data, error == nil else {
                return
            }
            
            // convert to JSON
            do {
                let vegetablesMap = try JSONDecoder().decode([VegetableMap].self, from: data)
                DispatchQueue.main.async {
                    self?.vegetablesMap = vegetablesMap
                }
            }
            catch {
                print(error)
            }
        }
        task.resume()
    }
}

struct MapView: View {
    @StateObject var viewModelMap = ViewMapModel()
    @State private var selectedAnnotation: Location? = nil
    @State private var mapRegion = MKCoordinateRegion(center: CLLocationCoordinate2D(latitude: -34.4110, longitude: 150.8948), span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05))
    
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
            
            Map(coordinateRegion: $mapRegion, annotationItems: locations) { location in MapAnnotation(coordinate: location.coordinate) {
                    ForEach(viewModelMap.vegetablesMap, id: \.self) { vegetableMap in
                        ZStack {
                            Circle()
                                .fill(Color(red: 1.0, green: 0.5, blue: 0.5))
                                .frame(width: 44, height: 44)
                                //.shadow(radius: 2)
                                .overlay(
                                    Circle()
                                        .stroke(Color.black, lineWidth: 2)
                                )
                            Text("$\(vegetableMap.price, specifier: "%.2f")")
                                .foregroundColor(.black)
                                .font(.system(size: 12))
                        }

                    }
                }
            }
            .onAppear {
                viewModelMap.fetch()
            }
        }.ignoresSafeArea(.all, edges: .top)
        
    }
}

struct MapView_Previews: PreviewProvider {
    static var previews: some View {
        MapView()
    }
}
