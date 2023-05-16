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


struct Supermarket: Hashable, Codable, Identifiable {
    let id = UUID()
    let sname: String
    let slatitude: String
    let slongitude: String
    let saddress: String
}

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
    @State private var searchQuery = ""
    @State private var selectedAnnotation: Supermarket? = nil
    @State private var mapRegion = MKCoordinateRegion(center: CLLocationCoordinate2D(latitude: -34.4110, longitude: 150.8948), span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05))
    @State private var isShowingAlert = false
    @Environment(\.colorScheme) var colorScheme
    
    var filteredSupermarkets: [Supermarket] {
        if searchQuery.isEmpty {
            return viewModelMap.supermarkets
        } else {
            return viewModelMap.supermarkets.filter { supermarket in
                supermarket.sname.localizedCaseInsensitiveContains(searchQuery)
            }
        }
    }
    
    var body: some View {
        NavigationView {
            ZStack {
                Map(coordinateRegion: $mapRegion, annotationItems: filteredSupermarkets) { supermarket in
                    MapAnnotation(coordinate: CLLocationCoordinate2D(latitude: Double(supermarket.slatitude) ?? 0.0, longitude: Double(supermarket.slongitude) ?? 0.0)) {
                        VStack {
                            Image(systemName: "mappin")
                                .resizable()
                                .frame(width: 10, height: 32)
                                .foregroundColor(.red)
                            ZStack {
                                
                                Rectangle()
                                    .foregroundColor(.blue)
                                Text(supermarket.sname)
                                    //.foregroundColor(.primary)
                                    .bold()
                                    .foregroundColor(.white)
                                    .font(.system(size: 14))
                                    .lineLimit(1)
                                    .truncationMode(.tail)
                            }
                            
                        }
                        .onTapGesture {
                            selectedAnnotation = supermarket
                            isShowingAlert = true
                        }
                    }
                }
                VStack {
                    TextField("Search vegetables", text: $searchQuery)
                        .padding()
                        .background(colorScheme == .dark ? Color.black : Color.white)
                        .foregroundColor(colorScheme == .dark ? Color.white : Color.black)
                        .cornerRadius(8)
                        .padding(.horizontal)
                        .offset(y: 60)
                        .shadow(radius: 4)
                        //.accentColor(.white)
                        //.background(Color(UIColor.systemBackground))
                    Spacer()
                }
                
            }
            //.searchable(text: $searchQuery, prompt: "Search")
            .edgesIgnoringSafeArea(.top)
            .alert(isPresented: $isShowingAlert) {
                guard let selectedAnnotation = selectedAnnotation else {
                    return Alert(title: Text("Error"), message: Text("An error occurred."), dismissButton: .default(Text("OK")))
                }
                
                return Alert(
                    title: Text(selectedAnnotation.sname),
                    message:
                        Text(selectedAnnotation.slatitude),
                    primaryButton: .default(Text("Report Mismatch")),
                    secondaryButton: .default(Text("Back to Map"), action: {
                        // Perform action to go to Home view
                    })
                )
            }
            //.navigationBarTitle("Stores")
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
