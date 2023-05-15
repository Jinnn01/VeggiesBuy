//
//  MapView.swift
//  VeggiesBuy
//
//  Created by Gabriel Komarnicki on 5/5/2023.
//

import SwiftUI
import MapKit

extension UIColor {
    convenience init(hex: String) {
        let scanner = Scanner(string: hex)
        scanner.currentIndex = hex.index(hex.startIndex, offsetBy: 1) // Skip the # character
        var rgbValue: UInt64 = 0
        scanner.scanHexInt64(&rgbValue)
        
        let red = CGFloat((rgbValue & 0xFF0000) >> 16) / 255.0
        let green = CGFloat((rgbValue & 0x00FF00) >> 8) / 255.0
        let blue = CGFloat(rgbValue & 0x0000FF) / 255.0
        
        self.init(red: red, green: green, blue: blue, alpha: 1.0)
    }
}

struct Location: Identifiable {
    let id = UUID()
    let name: String
    let coordinate: CLLocationCoordinate2D
}
/*
struct VegetableMap: Hashable, Codable {
    let sname: String
    let vname: String
    let price: Float
    let unit: String
    let slatitude: String
    let slongitude: String
    //let image: String
}*/


struct Supermarket: Hashable, Codable {
    let sname: String
    let slatitude: String
    let slongitude: String
}

// iosacademy tutorial
class ViewMapModel: ObservableObject {
    @Published var supermarkets: [Supermarket] = []
    //@State private var supermarkets: [Supermarket] = []
    
    func fetch() {
        //guard let url = URL(string: "https://iosacademy.io/api/v1/courses/index.php") else {
            //return
        guard let url = URL(string: "http://localhost:5006/store") else {
            return
        }
        
        let task = URLSession.shared.dataTask(with: url) { [weak self] data, _,
            error in
            guard let data = data, error == nil else {
                return
            }
            
            // convert to JSON
            do {
                let supermarkets = try JSONDecoder().decode([Supermarket].self, from: data)
                DispatchQueue.main.async {
                    self?.supermarkets = supermarkets
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
        NavigationView {
            VStack {
                List {
                    ForEach(viewModelMap.supermarkets, id: \.self) { supermarket in
                        HStack {
                            Text(supermarket.sname)
                                .bold()
                            //Text("$\(vegetable.price, specifier: "%.2f") per \(vegetable.unit)")
                            Spacer()
                            Text(supermarket.slatitude)
                            Text(supermarket.slongitude)
                        }
                        
                        .padding(3)
                    }
                }
                
                /*
                 List {
                 // ideally the id should be unique
                 ForEach(products, id: \.shopName) { product in
                 Text("\(product.shopName)")
                 Text("\(product.address.streetAddress)")
                 }
                 }*/
                
                /*
                 List {
                 // ideally the id should be unique
                 ForEach(filteredItems, id: \.self) { product in
                 Text(product)
                 }
                 }*/
                
                //LazyVGrid
            }
            //.searchable(text: $searchText, prompt: "Search")
            .navigationBarTitle("Stores")
            // from the iosacademy tutorial
            
            .onAppear {
                viewModelMap.fetch()
            }
        }
    }
    
    struct MapView_Previews: PreviewProvider {
        static var previews: some View {
            MapView()
        }
    }
}
