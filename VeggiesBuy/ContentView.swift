//
//  ContentView.swift
//  VeggiesBuy
//
//  Created by Gabriel Komarnicki on 5/5/2023.
//

import SwiftUI
import CoreData
import MapKit

/*
struct Location: Identifiable {
    let id = UUID()
    let name: String
    let coordinate: CLLocationCoordinate2D
}*/

struct ContentView: View {
    
    var body: some View {
        ZStack {
            Color.themeBackground
                .edgesIgnoringSafeArea(/*@START_MENU_TOKEN@*/.all/*@END_MENU_TOKEN@*/)
            
            TabView {
                HomeView()
                    .tabItem {
                        Image(systemName: "house.fill")
                        Text("Home")
                    }
                
                MapView()
                    .tabItem {
                        Image(systemName: "map.fill")
                        Text("Map")
                    }
                
                UploadView()
                    .tabItem {
                        Image(systemName: "tray.and.arrow.up.fill")
                        Text("Upload")
                    }
                /*
                RewardsView()
                    .tabItem {
                        Image(systemName: "trophy.fill")
                        Text("Rewards")
                    }*/
            }.accentColor(Color(UIColor(hex: "19AA5C")))
            
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
