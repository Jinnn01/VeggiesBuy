//
//  ItemDetailSheet.swift
//  VeggiesBuy
//
//  Created by Gabriel Komarnicki on 14/5/2023.
//

import SwiftUI
import MapKit

struct ItemDetailSheet: View {
    let vegetableMap: VegetableMap
    //let location: Location
    let coordinate: CLLocationCoordinate2D
    
    var body: some View {
        VStack {
            Text("Price: \(vegetableMap.price)")
            Text("Store Address: \(coordinate.slatitude), \(coordinate.slongitude)")
            
            // Additional details or content
            
            Spacer()
            
            Button("Close") {
                // Dismiss the sheet
            }
        }
        .padding()
    }
}

struct ItemDetailSheet_Previews: PreviewProvider {
    static var previews: some View {
        ItemDetailSheet(vegetableMap: <#VegetableMap#>, coordinate: <#T##CLLocationCoordinate2D#>)
    }
}
