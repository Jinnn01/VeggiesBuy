//
//  Vegetable.swift
//  VeggiesBuy
//
//  Created by Gabriel Komarnicki on 12/5/2023.
//

import Foundation
import SwiftUI

struct Grocery: Hashable, Codable {
    let sname: String
    let vname: String
    let price: Float
    let unit: String
    //let image: String
}

// iosacademy tutorial
class ViewModelGrocery: ObservableObject {
    @Published var groceries: [Grocery] = []
    
    func fetch() {
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
                let groceries = try JSONDecoder().decode([Grocery].self, from: data)
                DispatchQueue.main.async {
                    self?.groceries = groceries
                }
            }
            catch {
                print(error)
            }
        }
        task.resume()
    }
}


